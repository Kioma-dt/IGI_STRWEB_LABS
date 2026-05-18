from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from django.http import HttpRequest

SESSION_CART_KEY = "store_cart"



def _cart_raw(request: HttpRequest) -> dict[str, int]:
    raw = request.session.get(SESSION_CART_KEY)

    if not isinstance(raw, dict):
        return {}

    out: dict[str, int] = {}

    for k, v in raw.items():
        try:
            q = int(v)
        except (TypeError, ValueError):
            continue

        if q > 0:
            out[str(k)] = min(q, 999)

    return out


def _save_cart(request: HttpRequest, data: dict[str, int]) -> None:
    request.session[SESSION_CART_KEY] = data
    request.session.modified = True




def _cart_key(product_id: UUID, supplier_id: UUID | None) -> str:
    return f"{product_id}:{supplier_id}" if supplier_id else str(product_id)


def _parse_key(key: str) -> tuple[UUID, UUID | None]:
    parts = key.split(":")
    product_id = UUID(parts[0])
    supplier_id = UUID(parts[1]) if len(parts) > 1 and parts[1] != "None" else None
    return product_id, supplier_id



def cart_add(
    request: HttpRequest,
    product_id: UUID,
    quantity: int = 1,
    supplier_id: UUID | None = None,
    price: Decimal | None = None,
) -> None:
    if quantity < 1:
        return

    data = _cart_raw(request)

    key = _cart_key(product_id, supplier_id)

    data[key] = min(data.get(key, 0) + quantity, 999)

    _save_cart(request, data)


def cart_set_quantity(
    request: HttpRequest,
    product_id: UUID,
    quantity: int,
    supplier_id: UUID | None = None,
) -> None:
    data = _cart_raw(request)

    key = _cart_key(product_id, supplier_id)

    if quantity < 1:
        data.pop(key, None)
    else:
        data[key] = min(quantity, 999)

    _save_cart(request, data)


def cart_clear(request: HttpRequest) -> None:
    request.session.pop(SESSION_CART_KEY, None)
    request.session.modified = True


def cart_count(request: HttpRequest) -> int:
    return sum(_cart_raw(request).values())


@dataclass(frozen=True)
class CartLineView:
    product_id: UUID
    supplier_id: UUID | None
    product_name: str
    sku: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal


def cart_lines(request: HttpRequest) -> tuple[list[CartLineView], Decimal]:
    from apps.catalog.models import Product
    from apps.suppliers.models import ProductSupplier

    raw = _cart_raw(request)

    if not raw:
        return [], Decimal("0.00")

    parsed: list[tuple[UUID, UUID | None, int]] = []

    product_ids: set[UUID] = set()

    for key, qty in raw.items():
        pid, sid = _parse_key(key)
        parsed.append((pid, sid, qty))
        product_ids.add(pid)

    products = {
        p.id: p
        for p in Product.objects.filter(
            id__in=product_ids,
            is_deleted=False,
            is_active=True,
        )
    }

    lines: list[CartLineView] = []
    subtotal = Decimal("0.00")

    for pid, sid, qty in parsed:
        product = products.get(pid)
        if not product:
            continue

        unit = product.base_price

        if sid:
            link = ProductSupplier.objects.filter(
                product_id=pid,
                supplier_id=sid,
            ).first()

            if link:
                unit = link.last_purchase_price

        lt = (unit * qty).quantize(Decimal("0.01"))
        subtotal += lt

        lines.append(
            CartLineView(
                product_id=pid,
                supplier_id=sid,
                product_name=product.name,
                sku=product.sku,
                quantity=qty,
                unit_price=unit,
                line_total=lt,
            )
        )

    return lines, subtotal.quantize(Decimal("0.01"))