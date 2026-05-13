from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.suppliers.api.serializers import SupplierReadSerializer
from apps.suppliers.repositories.supplier_repository import SupplierRepository
from apps.users.permissions import django_permission


class SupplierListView(APIView):
    permission_classes = [IsAuthenticated, django_permission("users.view_suppliers")]

    def get(self, request, *args, **kwargs) -> Response:
        page = SupplierRepository().list(page=1, page_size=100)
        return Response(SupplierReadSerializer(page.items, many=True).data)
