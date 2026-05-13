"""Pure domain types (dataclasses) without Django or ORM imports."""

from .catalog import (
    Category,
    Product,
    ProductStock,
    ProductSupplierLink,
    Supplier,
)
from .content import (
    CompanyInfo,
    Contact,
    FAQ,
    NewsArticle,
    Review,
    Vacancy,
)
from .orders import Order, OrderItem, Purchase, PurchaseItem
from .promotions import PromoCode
from .users import CustomerProfile, EmployeeProfile, User

__all__ = [
    "Category",
    "CompanyInfo",
    "Contact",
    "CustomerProfile",
    "EmployeeProfile",
    "FAQ",
    "NewsArticle",
    "Order",
    "OrderItem",
    "Product",
    "ProductStock",
    "ProductSupplierLink",
    "PromoCode",
    "Purchase",
    "PurchaseItem",
    "Review",
    "Supplier",
    "User",
    "Vacancy",
]
