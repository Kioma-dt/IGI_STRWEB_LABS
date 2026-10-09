from __future__ import annotations

import logging
from decimal import Decimal
from uuid import UUID

from django.db import transaction

from application.dto.product import (
    RestockProductDTO,
    SetBasePriceDTO,
    StockCheckResultDTO,
)
from apps.catalog.repositories.product_repository import ProductRepository
from apps.catalog.repositories.product_stock_repository import ProductStockRepository
from core.exceptions import ProductNotFoundError

logger = logging.getLogger(__name__)


class ProductService:
    """Retail product operations: pricing and stock (no HTTP)."""

    def __init__(
        self,
        *,
        products: ProductRepository | None = None,
        stocks: ProductStockRepository | None = None,
    ) -> None:
        self._products = products or ProductRepository()
        self._stocks = stocks or ProductStockRepository()

    @transaction.atomic
    def set_base_price(self, payload: SetBasePriceDTO) -> None:
        product = self._products.get_by_id(payload.product_id)
        if product is None or not product.is_active or product.is_deleted:
            raise ProductNotFoundError("Product not found or inactive.")
        self._products.update(
            payload.product_id,
            {"base_price": payload.new_price},
        )
        logger.info("Updated base price for product %s", payload.product_id)

    @transaction.atomic
    def restock(self, payload: RestockProductDTO) -> int:
        product = self._products.get_by_id(payload.product_id)
        if product is None or product.is_deleted:
            raise ProductNotFoundError("Product not found.")
        self._stocks.ensure_stock_row(payload.product_id, initial_quantity=0)
        stock = self._stocks.get_for_product(payload.product_id, for_update=True)
        assert stock is not None
        new_qty = int(stock.quantity_on_hand) + payload.quantity_delta
        if new_qty < 0:
            from core.exceptions import InsufficientStockError

            raise InsufficientStockError("Restock would make quantity negative.")
        self._stocks.set_quantity(stock, new_qty)
        logger.info(
            "Restocked product %s by %s (new qty=%s)",
            payload.product_id,
            payload.quantity_delta,
            new_qty,
        )
        return new_qty

    def check_stock(self, product_id: UUID, requested_quantity: int) -> StockCheckResultDTO:
        if requested_quantity < 0:
            from core.exceptions import BusinessValidationError

            raise BusinessValidationError("requested_quantity cannot be negative.")
        stock = self._stocks.get_for_product(product_id, for_update=False)
        available = int(stock.quantity_on_hand) if stock is not None else 0
        return StockCheckResultDTO(
            product_id=product_id,
            available=available,
            requested=requested_quantity,
            sufficient=available >= requested_quantity,
        )
