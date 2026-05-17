from __future__ import annotations

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView
from django_filters.views import FilterView

from application.services.shop_staff_services import (
    ShopStaffCatalogService,
    ShopStaffNewsService,
    ShopStaffOrderService,
    ShopStaffPromoService,
    ShopStaffReviewService,
    ShopStaffSupplierService,
)
from apps.catalog.forms import CategoryForm, ProductCreateForm, ProductUpdateForm
from apps.catalog.models import Category, Product
from apps.news.forms import NewsArticleForm
from apps.news.models import NewsArticle
from apps.orders.forms import OrderCreateForm, OrderForm
from apps.orders.models import Order
from apps.promotions.forms import PromoCodeForm
from apps.promotions.models import PromoCode
from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review
from apps.suppliers.forms import SupplierForm
from apps.suppliers.models import Supplier
from apps.users import roles
from presentation.web.filtersets import (
    CategoryFilter,
    NewsArticleFilter,
    OrderFilter,
    ProductFilter,
    PromoCodeFilter,
    ReviewFilter,
    SupplierFilter,
)
from presentation.web.mixins import (
    AdminRequiredMixin,
    EmployeeRequiredMixin,
    StaffFilterListContextMixin,
    StaffRequiredMixin,
)


def _employee_suppliers_qs(user):
    profile = getattr(user, "employee_profile", None)
    if profile is None or profile.is_deleted:
        return Supplier.objects.none()
    return profile.suppliers.filter(is_deleted=False)


def _restrict_suppliers_for_limited_employee(user, queryset):
    if roles.is_employee_limited(user):
        return queryset.filter(pk__in=_employee_suppliers_qs(user).values("pk"))
    return queryset


def _restrict_orders_for_limited_employee(user, queryset):
    if not roles.is_employee_limited(user):
        return queryset
    supplier_ids = _employee_suppliers_qs(user).values("pk")
    return queryset.filter(items__product__suppliers__in=supplier_ids).distinct()


class StaffPortalHomeView(EmployeeRequiredMixin, View):
    """Role-aware staff home: employee -> sales, admin -> full catalog."""

    def get(self, request, *args, **kwargs):
        target = "web_shop:category-list" if roles.is_admin(request.user) else "web_shop:order-list"
        return HttpResponseRedirect(reverse(target))

# --- Categories ---


# --- Products ---


class ProductListView(AdminRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Product
    filterset_class = ProductFilter
    paginate_by = 20
    template_name = "web/catalog/product_list.html"
    context_object_name = "products"
    sort_links = (
        ("-created_at", "Newest"),
        ("name", "Name A–Z"),
        ("sku", "SKU A–Z"),
        ("base_price", "Price ↑"),
        ("-base_price", "Price ↓"),
    )

    def get_queryset(self):
        svc = ShopStaffCatalogService()
        return svc.products_base_queryset().order_by(
            svc.product_ordering(self.request.GET.get("ordering")),
        )


class ProductDetailView(AdminRequiredMixin, DetailView):
    model = Product
    template_name = "web/catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return ShopStaffCatalogService().products_detail_queryset()


class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "web/catalog/product_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffCatalogService()
        inst = form.save(commit=False)
        initial = int(form.cleaned_data.get("initial_stock") or 0)
        svc.persist_new_product(inst, initial_stock=initial)
        messages.success(self.request, "Product created.")
        return HttpResponseRedirect(reverse("web_shop:product-detail", kwargs={"pk": inst.pk}))


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = "web/catalog/product_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffCatalogService()
        svc.persist_product_update(form.save(commit=False))
        messages.success(self.request, "Product updated.")
        return HttpResponseRedirect(reverse("web_shop:product-detail", kwargs={"pk": self.object.pk}))


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = "web/confirm_delete.html"
    success_url = reverse_lazy("web_shop:product-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        ShopStaffCatalogService().delete_product(self.object)
        messages.success(request, "Product deleted.")
        return HttpResponseRedirect(str(self.success_url))


# --- Suppliers ---


class SupplierListView(EmployeeRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Supplier
    filterset_class = SupplierFilter
    paginate_by = 20
    template_name = "web/suppliers/supplier_list.html"
    context_object_name = "suppliers"
    sort_links = (
        ("-created_at", "Newest"),
        ("name", "Name A–Z"),
        ("-is_active", "Active first"),
    )

    def get_queryset(self):
        svc = ShopStaffSupplierService()
        qs = svc.suppliers_base_queryset().order_by(
            svc.supplier_ordering(self.request.GET.get("ordering")),
        )
        return _restrict_suppliers_for_limited_employee(self.request.user, qs)


class SupplierDetailView(EmployeeRequiredMixin, DetailView):
    model = Supplier
    template_name = "web/suppliers/supplier_detail.html"
    context_object_name = "supplier"

    def get_queryset(self):
        return _restrict_suppliers_for_limited_employee(
            self.request.user,
            Supplier.objects.filter(is_deleted=False).prefetch_related("products"),
        )


class SupplierCreateView(AdminRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "web/suppliers/supplier_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffSupplierService()
        obj = form.save(commit=False)
        svc.persist_supplier(obj)
        messages.success(self.request, "Supplier created.")
        return HttpResponseRedirect(reverse("web_shop:supplier-detail", kwargs={"pk": obj.pk}))


class SupplierUpdateView(AdminRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "web/suppliers/supplier_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffSupplierService()
        svc.persist_supplier(form.save(commit=False))
        messages.success(self.request, "Supplier updated.")
        return HttpResponseRedirect(reverse("web_shop:supplier-detail", kwargs={"pk": self.object.pk}))


class SupplierDeleteView(AdminRequiredMixin, DeleteView):
    model = Supplier
    template_name = "web/confirm_delete.html"
    success_url = reverse_lazy("web_shop:supplier-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        ShopStaffSupplierService().delete_supplier(self.object)
        messages.success(request, "Supplier deleted.")
        return HttpResponseRedirect(str(self.success_url))


# --- Orders ---


class OrderListView(EmployeeRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Order
    filterset_class = OrderFilter
    paginate_by = 20
    template_name = "web/orders/order_list.html"
    context_object_name = "orders"
    sort_links = (
        ("-ordered_at", "Order date ↓"),
        ("ordered_at", "Order date ↑"),
        ("status", "Status A–Z"),
        ("-total_amount", "Total ↓"),
        ("total_amount", "Total ↑"),
    )

    def get_queryset(self):
        svc = ShopStaffOrderService()
        qs = svc.orders_base_queryset().order_by(
            svc.order_ordering(self.request.GET.get("ordering")),
        )
        return _restrict_orders_for_limited_employee(self.request.user, qs)


class OrderDetailView(EmployeeRequiredMixin, DetailView):
    model = Order
    template_name = "web/orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        qs = ShopStaffOrderService().orders_detail_queryset()
        return _restrict_orders_for_limited_employee(self.request.user, qs)


class OrderCreateView(AdminRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "web/orders/order_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffOrderService()
        obj = form.save(commit=False)
        svc.create_empty_order(obj)
        messages.success(self.request, "Order created.")
        return HttpResponseRedirect(reverse("web_shop:order-detail", kwargs={"pk": obj.pk}))


class OrderUpdateView(AdminRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "web/orders/order_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffOrderService()
        svc.persist_order(form.save(commit=False))
        messages.success(self.request, "Order updated.")
        return HttpResponseRedirect(reverse("web_shop:order-detail", kwargs={"pk": self.object.pk}))


class OrderDeleteView(AdminRequiredMixin, DeleteView):
    model = Order
    template_name = "web/confirm_delete.html"
    success_url = reverse_lazy("web_shop:order-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        ShopStaffOrderService().delete_order(self.object)
        messages.success(request, "Order deleted.")
        return HttpResponseRedirect(str(self.success_url))


