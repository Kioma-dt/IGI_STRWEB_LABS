"""Data transfer objects for the application layer."""

from application.dto.orders import (
    OrderLineInputDTO,
    OrderPlacedResultDTO,
    OrderTotalsPreviewDTO,
    PlaceOrderDTO,
)
from application.dto.product import (
    RestockProductDTO,
    SetBasePriceDTO,
    StockCheckResultDTO,
)
from application.dto.promo import ApplyPromoInputDTO, PromoDiscountResultDTO
from application.dto.review import CreateReviewDTO
from application.dto.statistics import ShopStatisticsDTO
from application.dto.supplier import UpdateSupplyPriceDTO
from application.dto.user import AssignRoleDTO, RemoveRoleDTO

__all__ = [
    "ApplyPromoInputDTO",
    "AssignRoleDTO",
    "CreateReviewDTO",
    "OrderLineInputDTO",
    "OrderPlacedResultDTO",
    "OrderTotalsPreviewDTO",
    "PlaceOrderDTO",
    "PromoDiscountResultDTO",
    "RemoveRoleDTO",
    "RestockProductDTO",
    "SetBasePriceDTO",
    "ShopStatisticsDTO",
    "StockCheckResultDTO",
    "UpdateSupplyPriceDTO",
]
