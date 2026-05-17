from __future__ import annotations

from apps.users import roles
from presentation.web.cart import cart_count


def store_cart(request):
    """Количество позиций в корзине для навигации витрины."""
    return {"cart_items": cart_count(request)}


def user_roles(request):
    """Role flags for template-level access hints/navigation."""
    user = request.user
    return {
        "is_super_admin": roles.is_super_admin(user),
        "is_admin_role": roles.is_admin(user),
        "is_employee_role": roles.is_employee(user),
        "is_employee_limited": roles.is_employee_limited(user),
        "is_customer_role": roles.is_customer(user),
    }

