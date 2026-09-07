from __future__ import annotations

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django_filters.views import FilterView

from apps.catalog.forms import ProductCreateForm, ProductUpdateForm
from apps.catalog.models import Product
from apps.orders.models import Order, PurchaseItem
from apps.suppliers.forms import SupplierForm
from apps.suppliers.models import Supplier
from presentation.filtersets import ProductFilter, SupplierFilter, OrderFilter
from presentation.mixins import AdminRequiredMixin, StaffFilterListContextMixin
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
from apps.suppliers.forms import SupplierForm, ProductSupplierFormSet
from apps.suppliers.models import Supplier
from apps.users import roles
from presentation.filtersets import (
    CategoryFilter,
    NewsArticleFilter,
    OrderFilter,
    ProductFilter,
    PromoCodeFilter,
    ReviewFilter,
    SupplierFilter,
)
from presentation.mixins import (
    AdminRequiredMixin,
    EmployeeRequiredMixin,
    StaffFilterListContextMixin,
    StaffRequiredMixin,
)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["formset"] = ProductSupplierFormSet(self.request.POST)
        else:
            context["formset"] = ProductSupplierFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if not formset.is_valid():
            return self.form_invalid(form)

        self.object = form.save()

        formset.instance = self.object
        formset.save()

        messages.success(self.request, f"Поставщик «{self.object.name}» создан.")

        return HttpResponseRedirect(
            reverse("admin_panel:supplier-detail", kwargs={"pk": self.object.pk})
        )


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



from django.db.models import Sum, F, ExpressionWrapper, DecimalField

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
            .annotate(
                computed_total=Sum("items__line_total")
            )
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
            .annotate(
                computed_total=Sum("items__line_total")
            )
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        order_items = list(self.object.items.all())

        product_ids = [it.product_id for it in order_items]

        purchase_price_by_product = {}

        if product_ids:
            for pi in (
                PurchaseItem.objects.filter(
                    is_deleted=False,
                    product_id__in=product_ids
                )
                .select_related("purchase")
                .order_by("product_id", "-purchase__ordered_at")
            ):
                purchase_price_by_product.setdefault(
                    pi.product_id,
                    pi.purchase_price
                )

        ctx["sales_rows"] = [
            {
                "item": item,
                "purchase_price": purchase_price_by_product.get(item.product_id),
                "has_purchase_price": item.product_id in purchase_price_by_product,
                "purchase_total": (
                    purchase_price_by_product.get(item.product_id) * item.quantity
                    if purchase_price_by_product.get(item.product_id) is not None
                    else None
                ),
            }
            for item in order_items
        ]

        ctx["computed_total"] = self.object.computed_total or 0

        return ctx

class CategoryListView(AdminRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Category
    filterset_class = CategoryFilter
    paginate_by = 20
    template_name = "admin/catalog/category_list.html"
    context_object_name = "categories"
    sort_links = (
        ("-created_at", "Newest"),
        ("name", "Name A–Z"),
        ("slug", "Slug A–Z"),
    )

    def get_queryset(self):
        svc = ShopStaffCatalogService()
        return svc.categories_base_queryset().order_by(
            svc.category_ordering(self.request.GET.get("ordering")),
        )


class CategoryDetailView(AdminRequiredMixin, DetailView):
    model = Category
    template_name = "admin/catalog/category_detail.html"
    context_object_name = "category"


class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "admin/catalog/category_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffCatalogService()
        obj = form.save(commit=False)
        svc.persist_category(obj)
        messages.success(self.request, "Category created.")
        return HttpResponseRedirect(reverse("admin_panel:category-detail", kwargs={"pk": obj.pk}))


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "admin/catalog/category_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffCatalogService()
        svc.persist_category(form.save(commit=False))
        messages.success(self.request, "Category updated.")
        return HttpResponseRedirect(reverse("admin_panel:category-detail", kwargs={"pk": self.object.pk}))


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy("admin_panel:category-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        ShopStaffCatalogService().delete_category(self.object)
        messages.success(request, "Category deleted.")
        return HttpResponseRedirect(str(self.success_url))
    
class ReviewListView(AdminRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Review
    filterset_class = ReviewFilter
    paginate_by = 20
    template_name = "admin/reviews/review_list.html"
    context_object_name = "reviews"
    sort_links = (
        ("-created_at", "Newest"),
        ("rating", "Rating ↑"),
        ("-rating", "Rating ↓"),
        ("title", "Title A–Z"),
    )

    def get_queryset(self):
        svc = ShopStaffReviewService()
        return svc.reviews_base_queryset().order_by(
            svc.review_ordering(self.request.GET.get("ordering")),
        )


class ReviewDetailView(AdminRequiredMixin, DetailView):
    model = Review
    template_name = "admin/reviews/review_detail.html"
    context_object_name = "review"


class ReviewCreateView(AdminRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "admin/reviews/review_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffReviewService()
        obj = form.save(commit=False)
        svc.persist_review(obj)
        messages.success(self.request, "Review created.")
        return HttpResponseRedirect(reverse("admin_panel:review-detail", kwargs={"pk": obj.pk}))


class ReviewUpdateView(AdminRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "admin/reviews/review_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffReviewService()
        svc.persist_review(form.save(commit=False))
        messages.success(self.request, "Review updated.")
        return HttpResponseRedirect(reverse("admin_panel:review-detail", kwargs={"pk": self.object.pk}))


class ReviewDeleteView(AdminRequiredMixin, DeleteView):
    model = Review
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy("admin_panel:review-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        ShopStaffReviewService().delete_review(self.object)
        messages.success(request, "Review deleted.")
        return HttpResponseRedirect(str(self.success_url))


# --- News ---


class NewsArticleListView(AdminRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = NewsArticle
    filterset_class = NewsArticleFilter
    paginate_by = 20
    template_name = "admin/news/article_list.html"
    context_object_name = "articles"
    sort_links = (
        ("-published_at", "Published ↓"),
        ("published_at", "Published ↑"),
        ("title", "Title A–Z"),
        ("-created_at", "Created ↓"),
    )

    def get_queryset(self):
        svc = ShopStaffNewsService()
        return svc.news_base_queryset().order_by(
            svc.news_ordering(self.request.GET.get("ordering")),
        )


class NewsArticleDetailView(AdminRequiredMixin, DetailView):
    model = NewsArticle
    template_name = "admin/news/article_detail.html"
    context_object_name = "article"


class NewsArticleCreateView(AdminRequiredMixin, CreateView):
    model = NewsArticle
    form_class = NewsArticleForm
    template_name = "admin/news/article_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffNewsService()
        obj = form.save(commit=False)
        svc.persist_article(obj)
        messages.success(self.request, "News article created.")
        return HttpResponseRedirect(reverse("admin_panel:news-detail", kwargs={"pk": obj.pk}))


class NewsArticleUpdateView(AdminRequiredMixin, UpdateView):
    model = NewsArticle
    form_class = NewsArticleForm
    template_name = "admin/news/article_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffNewsService()
        svc.persist_article(form.save(commit=False))
        messages.success(self.request, "News article updated.")
        return HttpResponseRedirect(reverse("admin_panel:news-detail", kwargs={"pk": self.object.pk}))


class NewsArticleDeleteView(AdminRequiredMixin, DeleteView):
    model = NewsArticle
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy("admin_panel:news-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        ShopStaffNewsService().delete_article(self.object)
        messages.success(request, "News article deleted.")
        return HttpResponseRedirect(str(self.success_url))



class PromoCodeListView(AdminRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = PromoCode
    filterset_class = PromoCodeFilter
    paginate_by = 20
    template_name = "admin/promotions/promo_list.html"
    context_object_name = "promos"
    sort_links = (
        ("-created_at", "Newest"),
        ("code", "Code A–Z"),
        ("valid_from", "Valid from ↑"),
        ("-discount_percent", "Discount % ↓"),
    )

    def get_queryset(self):
        svc = ShopStaffPromoService()
        return svc.promos_base_queryset().order_by(
            svc.promo_ordering(self.request.GET.get("ordering")),
        )


class PromoCodeDetailView(AdminRequiredMixin, DetailView):
    model = PromoCode
    template_name = "admin/promotions/promo_detail.html"
    context_object_name = "promo"


class PromoCodeCreateView(AdminRequiredMixin, CreateView):
    model = PromoCode
    form_class = PromoCodeForm
    template_name = "admin/promotions/promo_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffPromoService()
        obj = svc.persist_promo_from_form(form)
        messages.success(self.request, "Promo code created.")
        return HttpResponseRedirect(reverse("admin_panel:promo-detail", kwargs={"pk": obj.pk}))


class PromoCodeUpdateView(AdminRequiredMixin, UpdateView):
    model = PromoCode
    form_class = PromoCodeForm
    template_name = "admin/promotions/promo_form.html"

    def form_valid(self, form) -> HttpResponseRedirect:
        svc = ShopStaffPromoService()
        svc.persist_promo_from_form(form)
        messages.success(self.request, "Promo code updated.")
        return HttpResponseRedirect(reverse("admin_panel:promo-detail", kwargs={"pk": self.object.pk}))


class PromoCodeDeleteView(AdminRequiredMixin, DeleteView):
    model = PromoCode
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy("admin_panel:promo-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        ShopStaffPromoService().delete_promo(self.object)
        messages.success(request, "Promo code deleted.")
        return HttpResponseRedirect(str(self.success_url))

