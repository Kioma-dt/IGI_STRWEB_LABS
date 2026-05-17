from __future__ import annotations

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django_filters.views import FilterView

from apps.catalog.forms import ProductCreateForm, ProductUpdateForm
from apps.catalog.models import Product
from apps.orders.models import Order
from apps.suppliers.forms import SupplierForm
from apps.suppliers.models import Supplier
from presentation.web.filtersets import ProductFilter, SupplierFilter, OrderFilter
from presentation.web.mixins import AdminRequiredMixin, StaffFilterListContextMixin

# --- Products (Admin CRUD) ---


class AdminProductListView(AdminRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Product
    filterset_class = ProductFilter
    paginate_by = 20
    template_name = "admin/products/product_list.html"
    context_object_name = "products"
    sort_links = (
        ("-created_at", "Newest"),
        ("name", "Name A–Z"),
        ("sku", "SKU A–Z"),
        ("base_price", "Price ↑"),
        ("-base_price", "Price ↓"),
    )

    def get_queryset(self):
        return (
            Product.objects.filter(is_deleted=False)
            .select_related("category", "stock")
            .prefetch_related("suppliers")
            .order_by(self.request.GET.get("ordering") or "-created_at")
        )


class AdminProductDetailView(AdminRequiredMixin, DetailView):
    model = Product
    template_name = "admin/products/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False).select_related(
            "category", "stock"
        ).prefetch_related("suppliers")


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "admin/products/product_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        inst = form.save(commit=False)
        inst.save()
        messages.success(self.request, f"Товар «{inst.name}» создан.")
        return HttpResponseRedirect(reverse("admin_panel:product-detail", kwargs={"pk": inst.pk}))


class AdminProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = "admin/products/product_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        inst = form.save()
        messages.success(self.request, f"Товар «{inst.name}» обновлён.")
        return HttpResponseRedirect(reverse("admin_panel:product-detail", kwargs={"pk": inst.pk}))


class AdminProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy("admin_panel:product-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        messages.success(request, f"Товар «{self.object.name}» удалён.")
        return HttpResponseRedirect(str(self.success_url))


# --- Suppliers (Admin CRUD) ---


class AdminSupplierListView(AdminRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Supplier
    filterset_class = SupplierFilter
    paginate_by = 20
    template_name = "admin/suppliers/supplier_list.html"
    context_object_name = "suppliers"
    sort_links = (
        ("-created_at", "Newest"),
        ("name", "Name A–Z"),
        ("-is_active", "Active first"),
    )

    def get_queryset(self):
        return (
            Supplier.objects.filter(is_deleted=False)
            .prefetch_related("products")
            .order_by(self.request.GET.get("ordering") or "-created_at")
        )


class AdminSupplierDetailView(AdminRequiredMixin, DetailView):
    model = Supplier
    template_name = "admin/suppliers/supplier_detail.html"
    context_object_name = "supplier"

    def get_queryset(self):
        return Supplier.objects.filter(is_deleted=False).prefetch_related("products")


class AdminSupplierCreateView(AdminRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "admin/suppliers/supplier_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        obj = form.save()
        messages.success(self.request, f"Поставщик «{obj.name}» создан.")
        return HttpResponseRedirect(reverse("admin_panel:supplier-detail", kwargs={"pk": obj.pk}))


class AdminSupplierUpdateView(AdminRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "admin/suppliers/supplier_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        obj = form.save()
        messages.success(self.request, f"Поставщик «{obj.name}» обновлён.")
        return HttpResponseRedirect(reverse("admin_panel:supplier-detail", kwargs={"pk": obj.pk}))


class AdminSupplierDeleteView(AdminRequiredMixin, DeleteView):
    model = Supplier
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy("admin_panel:supplier-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        messages.success(request, f"Поставщик «{self.object.name}» удалён.")
        return HttpResponseRedirect(str(self.success_url))


# --- Sales (Orders - Admin View) ---


class AdminSalesListView(AdminRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Order
    filterset_class = OrderFilter
    paginate_by = 20
    template_name = "admin/sales/sales_list.html"
    context_object_name = "orders"
    sort_links = (
        ("-ordered_at", "Date ↓"),
        ("ordered_at", "Date ↑"),
        ("status", "Status A–Z"),
        ("-total_amount", "Total ↓"),
        ("total_amount", "Total ↑"),
    )

    def get_queryset(self):
        return (
            Order.objects.filter(is_deleted=False)
            .select_related("customer", "promo_code")
            .prefetch_related("items__product")
            .order_by(self.request.GET.get("ordering") or "-ordered_at")
        )


class AdminSalesDetailView(AdminRequiredMixin, DetailView):
    model = Order
    template_name = "admin/sales/sales_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return (
            Order.objects.filter(is_deleted=False)
            .select_related("customer", "promo_code")
            .prefetch_related("items__product")
        )
