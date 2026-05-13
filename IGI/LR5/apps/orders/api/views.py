from __future__ import annotations

from decimal import Decimal

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from application.dto.orders import OrderLineInputDTO, PlaceOrderDTO
from application.services.order_service import OrderService
from application.services.statistics_service import StatisticsService
from apps.orders.api.serializers import PlaceOrderRequestSerializer
from apps.orders.models import Order
from apps.users.permissions import django_permission
from core.exceptions import (
    AgeRestrictionViolationError,
    BusinessValidationError,
    CustomerNotFoundError,
    InsufficientStockError,
    InvalidPromoCodeError,
    ProductNotFoundError,
)


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated, django_permission("users.view_own_orders")]

    def get(self, request, *args, **kwargs) -> Response:
        profile = getattr(request.user, "customer_profile", None)
        if profile is None:
            return Response(
                {"detail": "Customer profile required."},
                status=status.HTTP_403_FORBIDDEN,
            )
        qs = Order.objects.filter(customer=profile, is_deleted=False).order_by("-ordered_at")
        data = [
            {
                "id": str(o.id),
                "reference_number": o.reference_number,
                "status": o.status,
                "total_amount": str(o.total_amount),
                "ordered_at": o.ordered_at.isoformat(),
            }
            for o in qs[:100]
        ]
        return Response(data)


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated, django_permission("users.place_order")]

    def post(self, request, *args, **kwargs) -> Response:
        profile = getattr(request.user, "customer_profile", None)
        if profile is None:
            return Response(
                {"detail": "Customer profile required."},
                status=status.HTTP_403_FORBIDDEN,
            )
        ser = PlaceOrderRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        raw_lines = ser.validated_data["lines"]
        promo = ser.validated_data.get("promo_code") or None
        if isinstance(promo, str):
            promo = promo.strip() or None
        lines = tuple(
            OrderLineInputDTO(product_id=row["product_id"], quantity=row["quantity"])
            for row in raw_lines
        )
        dto = PlaceOrderDTO(
            customer_id=profile.id,
            lines=lines,
            promo_code=promo,
            created_by_employee_id=None,
        )
        try:
            result = OrderService().place_order(dto)
        except CustomerNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except ProductNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except InsufficientStockError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidPromoCodeError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except AgeRestrictionViolationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except BusinessValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "order_id": str(result.order_id),
                "reference_number": result.reference_number,
                "subtotal": str(result.subtotal),
                "discount": str(result.discount),
                "total": str(result.total),
                "promo_code": result.promo_code,
            },
            status=status.HTTP_201_CREATED,
        )


class SalesStatisticsView(APIView):
    permission_classes = [IsAuthenticated, django_permission("users.view_sales")]

    def get(self, request, *args, **kwargs) -> Response:
        stats = StatisticsService().get_shop_statistics()
        return Response(
            {
                "orders_total_count": stats.orders_total_count,
                "orders_revenue": str(stats.orders_revenue),
                "active_products_count": stats.active_products_count,
                "published_reviews_count": stats.published_reviews_count,
                "low_stock_product_count": stats.low_stock_product_count,
                "active_suppliers_count": stats.active_suppliers_count,
            },
        )
