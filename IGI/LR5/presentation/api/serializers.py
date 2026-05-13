from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from application.services.shop_staff_services import ShopStaffCatalogService
from apps.catalog.models import Category, Product
from apps.news.models import NewsArticle
from apps.orders.models import Order, OrderItem
from apps.promotions.models import PromoCode
from apps.reviews.models import Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "parent",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs: dict) -> dict:
        parent = attrs.get("parent", getattr(self.instance, "parent", None))
        inst = self.instance
        if inst and parent and parent.pk == inst.pk:
            raise serializers.ValidationError("A category cannot be its own parent.")
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    initial_stock = serializers.IntegerField(
        write_only=True,
        required=False,
        default=0,
        min_value=0,
    )
    stock_quantity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "sku",
            "category",
            "description",
            "base_price",
            "age_restriction",
            "is_active",
            "initial_stock",
            "stock_quantity",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "stock_quantity", "created_at", "updated_at")

    def get_stock_quantity(self, obj: Product) -> int:
        stock = getattr(obj, "stock", None)
        if stock is None:
            return 0
        return int(stock.quantity_on_hand)

    def create(self, validated_data: dict) -> Product:
        initial = int(validated_data.pop("initial_stock", 0))
        product = Product(**validated_data)
        return ShopStaffCatalogService().persist_new_product(product, initial_stock=initial)

    def update(self, instance: Product, validated_data: dict) -> Product:
        validated_data.pop("initial_stock", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        return ShopStaffCatalogService().persist_product_update(instance)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "line_total",
        )
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "reference_number",
            "customer",
            "created_by",
            "promo_code",
            "status",
            "total_amount",
            "ordered_at",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "reference_number",
            "ordered_at",
            "items",
            "created_at",
            "updated_at",
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "product",
            "customer",
            "rating",
            "title",
            "body",
            "is_published",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = (
            "id",
            "title",
            "slug",
            "body",
            "published_at",
            "is_published",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = (
            "id",
            "code",
            "discount_percent",
            "valid_from",
            "valid_until",
            "max_uses",
            "current_uses",
            "is_active",
            "customers",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_discount_percent(self, value: Decimal) -> Decimal:
        if value < 0 or value > 100:
            raise serializers.ValidationError("Discount must be between 0 and 100.")
        return value
