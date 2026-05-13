from __future__ import annotations

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from application.dto.product import SetBasePriceDTO
from application.services.product_service import ProductService
from apps.catalog.api.serializers import ProductReadSerializer, ProductSetPriceSerializer
from apps.catalog.repositories.product_repository import ProductRepository
from apps.users.permissions import django_permission


class ProductListView(APIView):
    """Public product catalog (anonymous and authenticated)."""

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs) -> Response:
        repo = ProductRepository()
        page = repo.list(page=1, page_size=50)
        data = ProductReadSerializer(page.items, many=True).data
        return Response({"count": page.total_count, "results": data})


class ProductManageView(APIView):
    """Employee/admin: update catalog pricing (Django permission `users.manage_products`)."""

    permission_classes = [IsAuthenticated, django_permission("users.manage_products")]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = ProductSetPriceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ProductService().set_base_price(
            SetBasePriceDTO(
                product_id=serializer.validated_data["product_id"],
                new_price=serializer.validated_data["new_price"],
            ),
        )
        return Response(status=204)
