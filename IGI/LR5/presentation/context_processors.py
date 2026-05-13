from __future__ import annotations

from presentation.web.cart import cart_count


def store_cart(request):
    """Количество позиций в корзине для навигации витрины."""
    return {"cart_items": cart_count(request)}
