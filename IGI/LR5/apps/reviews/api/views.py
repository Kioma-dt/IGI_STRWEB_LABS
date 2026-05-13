from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reviews.api.serializers import ReviewCreateSerializer
from apps.reviews.models import Review
from apps.users.permissions import django_permission


class ReviewCreateView(APIView):
    permission_classes = [IsAuthenticated, django_permission("users.submit_product_review")]

    def post(self, request, *args, **kwargs) -> Response:
        profile = getattr(request.user, "customer_profile", None)
        if profile is None:
            return Response(
                {"detail": "Customer profile required."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.create(
            product_id=serializer.validated_data["product_id"],
            customer=profile,
            rating=serializer.validated_data["rating"],
            title=serializer.validated_data["title"].strip(),
            body=(serializer.validated_data.get("body") or "").strip(),
        )
        return Response(
            {"id": str(review.id), "product_id": str(review.product_id)},
            status=status.HTTP_201_CREATED,
        )
