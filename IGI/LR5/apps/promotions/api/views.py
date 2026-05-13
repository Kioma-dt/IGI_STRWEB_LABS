from __future__ import annotations

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.promotions.api.serializers import PromoCodeReadSerializer
from apps.promotions.models import PromoCode
from apps.users.permissions import django_permission


class ActivePromotionsListView(APIView):
    permission_classes = [IsAuthenticated, django_permission("users.view_active_promotions")]

    def get(self, request, *args, **kwargs) -> Response:
        today = timezone.now().date()
        qs = PromoCode.objects.all().active_on(today)[:200]
        return Response(PromoCodeReadSerializer(qs, many=True).data)
