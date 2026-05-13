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


def cart_add(request: HttpRequest, product_id: UUID, quantity: int = 1) -> None:
    if quantity < 1:
        return
    data = _cart_raw(request)
    pid = str(product_id)
    data[pid] = min(data.get(pid, 0) + quantity, 999)
    _save_cart(request, data)


def cart_set_quantity(request: HttpRequest, product_id: UUID, quantity: int) -> None:
    data = _cart_raw(request)
    pid = str(product_id)
    if quantity < 1:
        data.pop(pid, None)
    else:
        data[pid] = min(quantity, 999)
    _save_cart(request, data)


def cart_clear(request: HttpRequest) -> None:
    request.session.pop(SESSION_CART_KEY, None)
    request.session.modified = True


def cart_count(request: HttpRequest) -> int:
    return sum(_cart_raw(request).values())


@dataclass(frozen=True)
class CartLineView:
    product_id: UUID
    product_name: str
    sku: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal


def cart_lines(request: HttpRequest) -> tuple[list[CartLineView], Decimal]:
    from apps.catalog.models import Product

    raw = _cart_raw(request)
    if not raw:
        return [], Decimal("0.00")
    ids = [UUID(k) for k in raw]
    products = {
        p.id: p
        for p in Product.objects.filter(
            id__in=ids,
            is_deleted=False,
            is_active=True,
        ).select_related("category")
    }
    lines: list[CartLineView] = []
    subtotal = Decimal("0.00")
    for pid_str, qty in raw.items():
        try:
            pid = UUID(pid_str)
        except ValueError:
            continue
        p = products.get(pid)
        if p is None:
            continue
        unit = p.base_price
        lt = (unit * qty).quantize(Decimal("0.01"))
        subtotal += lt
        lines.append(
            CartLineView(
                product_id=p.id,
                product_name=p.name,
                sku=p.sku,
                quantity=qty,
                unit_price=unit,
                line_total=lt,
            ),
        )
    return lines, subtotal.quantize(Decimal("0.01"))
