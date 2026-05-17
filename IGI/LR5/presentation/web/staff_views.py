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


