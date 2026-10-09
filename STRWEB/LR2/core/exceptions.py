"""Domain / application errors (no HTTP coupling)."""


class DomainError(Exception):
    """Base class for expected business rule violations."""


class BusinessValidationError(DomainError):
    """Input failed business validation."""


class ProductNotFoundError(DomainError):
    """Requested product does not exist or is inactive."""


class CustomerNotFoundError(DomainError):
    """Requested customer profile does not exist."""


class OrderNotFoundError(DomainError):
    """Requested order does not exist."""


class InsufficientStockError(DomainError):
    """Not enough quantity on hand for the operation."""


class InvalidPromoCodeError(DomainError):
    """Promo code is missing, inactive, expired, exhausted, or not eligible."""


class AgeRestrictionViolationError(DomainError):
    """Customer does not meet product age restriction."""


class ProductSupplierLinkNotFoundError(DomainError):
    """No supplier link for the given product and supplier."""


class ReviewDuplicateError(DomainError):
    """A review with the same unique key already exists."""


class UserNotFoundError(DomainError):
    """User does not exist."""


class RoleManagementError(DomainError):
    """Role assignment or removal failed."""
