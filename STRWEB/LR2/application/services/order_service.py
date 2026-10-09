from __future__ import annotations

import logging
from collections import defaultdict
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from django.db import transaction

from application.dto.orders import (
    OrderLineInputDTO,
    OrderPlacedResultDTO,
    OrderTotalsPreviewDTO,
    PlaceOrderDTO,
)
from application.dto.promo import ApplyPromoInputDTO
from application.services.promo_code_service import PromoCodeService
from apps.catalog.models import Product
from apps.catalog.repositories.product_repository import ProductRepository
from apps.catalog.repositories.product_stock_repository import ProductStockRepository
from apps.orders.models import Order, OrderItem
from apps.orders.repositories.order_item_repository import OrderItemRepository
from apps.orders.repositories.order_repository import OrderRepository
from apps.promotions.models import PromoCode
from apps.users.models import CustomerProfile, EmployeeProfile
from core.exceptions import (
    AgeRestrictionViolationError,
    BusinessValidationError,
    CustomerNotFoundError,
    InsufficientStockError,
    InvalidPromoCodeError,
    ProductNotFoundError,
)

logger = logging.getLogger(__name__)


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _is_adult(birth_date: date | None) -> bool:
    if birth_date is None:
        return False
    return birth_date <= date.today() - timedelta(days=18 * 365)


class OrderService:
    """
    Purchase / order use-cases: stock checks, totals, promo application, persistence.

    HTTP layers must not call ORM directly; they call this service with DTOs.
    """

    def __init__(
        self,
        *,
        orders: OrderRepository | None = None,
        order_items: OrderItemRepository | None = None,
        stocks: ProductStockRepository | None = None,
        products: ProductRepository | None = None,
        promo_service: PromoCodeService | None = None,
    ) -> None:
        self._orders = orders or OrderRepository()
        self._order_items = order_items or OrderItemRepository()
        self._stocks = stocks or ProductStockRepository()
        self._products = products or ProductRepository()
        self._promo_service = promo_service or PromoCodeService()

    def preview_totals(self, dto: PlaceOrderDTO) -> OrderTotalsPreviewDTO:
        """Compute subtotal/discount/total without persisting (read-only path)."""
        self._validate_customer(dto.customer_id)
        merged = self._merge_lines(dto.lines)
        subtotal = self._compute_subtotal_readonly(merged)
        discount = self._discount_for_preview(dto, subtotal)
        total = _money(max(subtotal - discount, Decimal("0.00")))
        return OrderTotalsPreviewDTO(
            subtotal=_money(subtotal),
            discount=_money(discount),
            total=total,
        )

    @transaction.atomic
    def place_order(self, dto: PlaceOrderDTO) -> OrderPlacedResultDTO:
        customer = self._validate_customer(dto.customer_id)
        merged = self._merge_lines(dto.lines)
        product_ids = sorted(merged.keys())

        products = self._products.lock_active_by_ids(list(product_ids))

        for pid in product_ids:
            self._stocks.get_for_product(pid, for_update=True)

        self._assert_age_restrictions(customer, merged, products)

        line_rows: list[tuple[UUID, int, Decimal, Decimal]] = []
        subtotal = Decimal("0.00")
        for pid, qty in merged.items():
            p = products[pid]
            unit = _money(p.base_price)
            line_total = _money(unit * qty)
            subtotal += line_total
            line_rows.append((pid, qty, unit, line_total))

        subtotal = _money(subtotal)
        discount, promo_model = self._resolve_promo(dto, subtotal)
        total = _money(max(subtotal - discount, Decimal("0.00")))

        employee_id = self._validate_employee_optional(dto.created_by_employee_id)

        order = self._orders.create(
            {
                "customer_id": dto.customer_id,
                "created_by_id": employee_id,
                "total_amount": total,
                "status": Order.Status.NEW,
                "promo_code_id": promo_model.id if promo_model else None,
            },
        )

        items = [
            OrderItem(
                order=order,
                product_id=pid,
                quantity=qty,
                unit_price=unit,
                line_total=lt,
            )
            for pid, qty, unit, lt in line_rows
        ]
        self._order_items.bulk_create_items(items)

        for pid, qty, _unit, _lt in line_rows:
            self._decrement_stock(pid, qty)

        if promo_model is not None:
            self._promo_service.register_use(promo_model.id)

        logger.info(
            "Order placed id=%s ref=%s total=%s discount=%s",
            order.id,
            order.reference_number,
            total,
            discount,
        )
        return OrderPlacedResultDTO(
            order_id=order.id,
            reference_number=order.reference_number,
            subtotal=subtotal,
            discount=discount,
            total=total,
            promo_code=promo_model.code if promo_model else None,
        )

    def _discount_for_preview(self, dto: PlaceOrderDTO, subtotal: Decimal) -> Decimal:
        if not dto.promo_code:
            return Decimal("0.00")
        try:
            result = self._promo_service.evaluate_discount(
                ApplyPromoInputDTO(
                    promo_code=dto.promo_code,
                    customer_id=dto.customer_id,
                    order_subtotal=subtotal,
                ),
            )
        except InvalidPromoCodeError as exc:
            logger.warning("Promo preview rejected: %s", exc)
            raise
        return _money(result.discount_amount)

    def _resolve_promo(
        self,
        dto: PlaceOrderDTO,
        subtotal: Decimal,
    ) -> tuple[Decimal, PromoCode | None]:
        if not dto.promo_code:
            return Decimal("0.00"), None
        result = self._promo_service.evaluate_discount(
            ApplyPromoInputDTO(
                promo_code=dto.promo_code,
                customer_id=dto.customer_id,
                order_subtotal=subtotal,
            ),
        )
        promo_model = self._promo_service.get_promo_entity(result.promo_id)
        if result.promo_id is not None and promo_model is None:
            raise InvalidPromoCodeError("Promo code is no longer available.")
        return _money(result.discount_amount), promo_model

    @staticmethod
    def _merge_lines(lines: tuple[OrderLineInputDTO, ...]) -> dict[UUID, int]:
        merged: dict[UUID, int] = defaultdict(int)
        for line in lines:
            merged[line.product_id] += line.quantity
        return dict(merged)

    def _compute_subtotal_readonly(self, merged: dict[UUID, int]) -> Decimal:
        subtotal = Decimal("0.00")
        for pid, qty in merged.items():
            product = self._products.get_by_id(pid)
            if product is None or not product.is_active or product.is_deleted:
                raise ProductNotFoundError(f"Product not available: {pid}")
            subtotal += _money(product.base_price) * qty
        return _money(subtotal)

    def _validate_customer(self, customer_id: UUID) -> CustomerProfile:
        try:
            return CustomerProfile.objects.get(pk=customer_id, is_deleted=False)
        except CustomerProfile.DoesNotExist as exc:
            logger.warning("Customer not found: %s", customer_id)
            raise CustomerNotFoundError("Customer not found.") from exc

    @staticmethod
    def _validate_employee_optional(employee_id: UUID | None) -> UUID | None:
        if employee_id is None:
            return None
        if not EmployeeProfile.objects.filter(pk=employee_id, is_deleted=False).exists():
            raise BusinessValidationError("Employee profile not found.")
        return employee_id

    @staticmethod
    def _assert_age_restrictions(
        customer: CustomerProfile,
        merged: dict[UUID, int],
        products: dict[UUID, Product],
    ) -> None:
        for pid in merged:
            product = products[pid]
            if int(product.age_restriction) != Product.AgeRestriction.ADULT_18:
                continue
            if not _is_adult(customer.birth_date):
                logger.info("Age restriction failed for customer %s", customer.id)
                raise AgeRestrictionViolationError(
                    "Customer does not meet the 18+ requirement for one or more products.",
                )

    def _decrement_stock(self, product_id: UUID, quantity: int) -> None:
        stock = self._stocks.get_for_product(product_id, for_update=True)
        available = stock.quantity_on_hand if stock is not None else 0
        if available < quantity:
            raise InsufficientStockError(
                f"Insufficient stock for product {product_id}. "
                f"Available={available}, requested={quantity}.",
            )
        if stock is None:
            raise InsufficientStockError(f"No stock record for product {product_id}.")
        self._stocks.set_quantity(stock, available - quantity)
