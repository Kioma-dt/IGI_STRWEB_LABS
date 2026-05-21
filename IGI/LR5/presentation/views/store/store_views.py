from __future__ import annotations

from datetime import date, timezone
from datetime import datetime
from uuid import UUID

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django_filters.views import FilterView

from application.dto.orders import OrderLineInputDTO, PlaceOrderDTO
from application.services.order_service import OrderService
from apps.catalog.models import Product
from apps.common.models import CompanyInfo, Contact, FAQ, PickupPoint, Vacancy
from apps.news.models import NewsArticle
from apps.orders.models import Order
from apps.promotions.models import PromoCode
from apps.reviews.models import Review
from presentation.cart import (
    cart_add,
    cart_clear,
    cart_lines,
    cart_set_quantity,
)
from presentation.store_forms import (
    AddToCartForm,
    CheckoutForm,
    ContactMessageForm,
    CustomerSignupForm,
    EmployeeSignupForm,
    StoreProductFilter,
    StoreReviewForm,
    VacancyApplicationForm,
)
from core.exceptions import BusinessValidationError
from core.calendar import BirthdayCalendar

from infrastructure.genderize_client import GenderizeClient
from infrastructure.cat_fact_client import CatFactClient

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
from apps.suppliers.models import Supplier, ProductSupplier
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




class StorePaginationQueryMixin:
    """Preserve GET params except ``page`` for pagination links."""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.request.GET.copy()
        p.pop("page", None)
        ctx["pagination_query"] = p.urlencode()
        return ctx


class StoreHomeView(TemplateView):
    template_name = "store/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_products"] = (
            Product.objects.filter(is_deleted=False, is_active=True)
            .select_related("category")
            .order_by("-created_at")[:8]
        )
        return ctx


class StoreAboutView(TemplateView):
    template_name = "store/info/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["company"] = (
            CompanyInfo.objects.filter(is_deleted=False, is_current=True).first()
        )
        return ctx


class StoreNewsListView(StorePaginationQueryMixin, ListView):
    model = NewsArticle
    template_name = "store/info/news_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return (
            NewsArticle.objects.filter(is_deleted=False, is_published=True)
            .order_by("-published_at", "-created_at")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class StoreNewsDetailView(DetailView):
    model = NewsArticle
    template_name = "store/info/news_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return NewsArticle.objects.filter(is_deleted=False, is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class StoreFAQView(TemplateView):
    template_name = "store/info/faq.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["faq_list"] = FAQ.objects.filter(is_deleted=False).order_by(
            "sort_order",
            "created_at",
        )


        try:
            client = CatFactClient()

            fact = client.get_random_fact(max_length=150)

            ctx["cat_fact"] = fact.fact
        except Exception:
            ctx["cat_fact"] = None

        return ctx


class StoreContactsView(FormView):
    template_name = "store/info/contacts.html"
    form_class = ContactMessageForm
    success_url = reverse_lazy("store:contacts")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contacts"] = Contact.objects.filter(is_deleted=False).order_by(
            "-is_primary",
            "type",
        )
        ctx["company"] = (
            CompanyInfo.objects.filter(is_deleted=False, is_current=True).first()
        )
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request,
            "Сообщение принято (демо: данные не сохраняются на сервере). "
            "Проверьте поля формы — валидация прошла успешно.",
        )
        return super().form_valid(form)


class StorePrivacyView(TemplateView):
    template_name = "store/info/privacy.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class StoreVacancyListView(StorePaginationQueryMixin, ListView):
    model = Vacancy
    template_name = "store/info/vacancy_list.html"
    context_object_name = "vacancies"
    paginate_by = 15

    def get_queryset(self):
        return Vacancy.objects.filter(is_deleted=False, is_active=True).order_by(
            "-published_at",
            "title",
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class StoreVacancyApplyView(FormView):
    template_name = "store/info/vacancy_apply.html"
    form_class = VacancyApplicationForm

    def dispatch(self, request, *args, **kwargs):
        self.vacancy = get_object_or_404(
            Vacancy.objects.filter(is_deleted=False, is_active=True),
            pk=kwargs["pk"],
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["vacancy"] = self.vacancy
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Заявка на вакансию «{self.vacancy.title}» отправлена (демо, без сохранения в БД).",
        )
        return redirect("store:vacancy-list")


class StoreCatalogView(StorePaginationQueryMixin, FilterView):
    model = Product
    filterset_class = StoreProductFilter
    template_name = "store/products/catalog_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return (
            Product.objects.filter(is_deleted=False, is_active=True)
            .select_related("category")
            .order_by("name")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

class StoreProductDetailView(FormView):
    template_name = "store/products/product_detail.html"
    form_class = AddToCartForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            Product.objects.filter(is_deleted=False, is_active=True)
            .select_related("category"),
            pk=kwargs["pk"],
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["supplier"].queryset = Supplier.objects.filter(
            product_links__product=self.product,
            is_active=True,
        ).distinct()

        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["product"] = self.product

        ctx["reviews"] = (
            Review.objects.filter(
                is_deleted=False,
                is_published=True,
                product=self.product,
            )
            .select_related("customer")
            .order_by("-created_at")[:50]
        )

        ctx.setdefault("review_form", StoreReviewForm())

        ctx["suppliers"] = (
            ProductSupplier.objects
            .filter(product=self.product)
            .select_related("supplier")
        )

        return ctx

    def form_valid(self, form):
        supplier = form.cleaned_data["supplier"]
        quantity = form.cleaned_data["quantity"]

        link = ProductSupplier.objects.get(
            product=self.product,
            supplier=supplier,
        )

        price = link.last_purchase_price

        cart_add(
            self.request,
            self.product.id,
            quantity,
            supplier_id=supplier.id,
            price=price,
        )

        messages.success(
            self.request,
            f"Добавлено в корзину от поставщика {supplier.name}.",
        )

        return redirect("store:product-detail", pk=self.product.pk)

    def post(self, request, *args, **kwargs):
        if "submit_review" in request.POST:
            return self._post_review(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def _post_review(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('store:login')}?next={request.path}")

        profile = getattr(request.user, "customer_profile", None)
        if profile is None or profile.is_deleted:
            return redirect("store:product-detail", pk=self.product.pk)

        rf = StoreReviewForm(request.POST)

        if not rf.is_valid():
            ctx = self.get_context_data()
            ctx["review_form"] = rf
            return self.render_to_response(ctx)

        Review.objects.create(
            product=self.product,
            customer=profile,
            rating=rf.cleaned_data["rating"],
            title=rf.cleaned_data["title"],
            body=rf.cleaned_data.get("body") or "",
            is_published=True,
        )

        messages.success(request, "Отзыв опубликован.")
        return redirect("store:product-detail", pk=self.product.pk)


class StoreCartView(TemplateView):
    template_name = "store/products/cart.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lines, subtotal = cart_lines(self.request)
        ctx["lines"] = lines
        ctx["subtotal"] = subtotal
        ctx["checkout_form"] = CheckoutForm()
        return ctx

    def post(self, request, *args, **kwargs):
        if "clear" in request.POST:
            cart_clear(request)
            messages.info(request, "Корзина очищена.")
            return redirect("store:cart")
        for key, val in request.POST.items():
            if key.startswith("qty_"):
                try:
                    pid = UUID(key[4:])
                    qty = int(val)
                except (ValueError, TypeError):
                    continue
                cart_set_quantity(request, pid, qty)
        messages.success(request, "Количества обновлены.")
        return redirect("store:cart")


class StoreCheckoutView(LoginRequiredMixin, FormView):
    template_name = "store/info/checkout.html"
    form_class = CheckoutForm
    login_url = reverse_lazy("store:login")

    def get(self, request, *args, **kwargs):
        lines, _sub = cart_lines(request)
        if not lines:
            messages.warning(request, "Корзина пуста.")
            return redirect("store:cart")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lines, subtotal = cart_lines(self.request)
        ctx["lines"] = lines
        ctx["subtotal"] = subtotal
        return ctx

    def form_valid(self, form):
        profile = getattr(self.request.user, "customer_profile", None)
        if profile is None or profile.is_deleted:
            messages.error(self.request, "Оформление доступно только клиентам с профилем.")
            return redirect("store:signup")

        lines, _ = cart_lines(self.request)
        if not lines:
            messages.warning(self.request, "Корзина пуста.")
            return redirect("store:cart")

        dto_lines = tuple(
            OrderLineInputDTO(product_id=ln.product_id, quantity=ln.quantity)
            for ln in lines
        )
        promo = (form.cleaned_data.get("promo_code") or "").strip() or None
        dto = PlaceOrderDTO(
            customer_id=profile.id,
            lines=dto_lines,
            promo_code=promo,
            created_by_employee_id=None,
        )
        try:
            result = OrderService().place_order(dto)
        except BusinessValidationError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        except Exception as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)

        cart_clear(self.request)
        messages.success(
            self.request,
            f"Заказ создан. Номер: {result.reference_number}. Сумма: {result.total}.",
        )
        return redirect("store:account-orders")

    def get_success_url(self):
        return reverse("store:account-orders")


class StoreAccountView(LoginRequiredMixin, TemplateView):
    template_name = "store/accounts/account.html"
    login_url = reverse_lazy("store:login")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            profile = user.customer_profile
        except:
            profile = None

        try:
            employee_profile = user.employee_profile
        except:
            employee_profile = None

        ctx["profile"] = profile
        ctx["employee_profile"] = employee_profile

        full_name = None

        if profile:
            full_name = profile.full_name
        elif employee_profile:
            full_name = employee_profile.full_name

        predicted_gender = None

        try:
            if full_name:
                first_name = full_name.split()[0]

                client = GenderizeClient()
                result = client.get_gender(first_name)

                predicted_gender = result.gender
        except Exception as e:
            print(e)

        ctx["predicted_gender"] = predicted_gender

        offset = datetime.now().astimezone().utcoffset()

        hours = int(offset.total_seconds() // 3600)

        ctx["timezone"] = f"UTC{hours:+d}"

        today = datetime.now()

        birthday_day = today.day
        birthday_month = today.month
        birthday_year = today.year

        if profile and profile.birth_date:
            birthday_day = profile.birth_date.day
            birthday_month = profile.birth_date.month
            birthday_year = profile.birth_date.year

        cal = BirthdayCalendar(
            birthday_day=birthday_day,
            birthday_month=birthday_month
        )

        ctx["calendar_html"] = cal.formatmonth(
            birthday_year,
            birthday_month
        )

        ctx["calendar_title"] = today.strftime("%B %Y")

        return ctx


class StoreAccountOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "store/accounts/account_orders.html"
    context_object_name = "orders"
    paginate_by = 15
    login_url = reverse_lazy("store:login")

    def get_queryset(self):
        profile = getattr(self.request.user, "customer_profile", None)
        if profile is None:
            return Order.objects.none()
        return (
            Order.objects.filter(is_deleted=False, customer=profile)
            .order_by("-ordered_at")
            .prefetch_related("items__product")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.request.GET.copy()
        p.pop("page", None)
        ctx["pagination_query"] = p.urlencode()
        return ctx


class StoreReviewsView(StorePaginationQueryMixin, ListView):
    model = Review
    template_name = "store/info/reviews_list.html"
    context_object_name = "reviews"
    paginate_by = 20

    def get_queryset(self):
        return (
            Review.objects.filter(is_deleted=False, is_published=True)
            .select_related("product", "customer")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class StorePromosView(TemplateView):
    template_name = "store/info/promos_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        ctx["promos"] = PromoCode.objects.active_on(today).order_by("code")
        return ctx


class StorePickupPointsView(TemplateView):
    template_name = "store/info/pickup_points.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pickup_points"] = PickupPoint.objects.filter(
            is_deleted=False,
            is_active=True,
        ).order_by("name")
        return ctx


class StoreLoginView(LoginView):
    template_name = "store/accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.request.GET.get("next") or reverse("store:home")


class StoreLogoutView(LogoutView):
    next_page = reverse_lazy("store:home")


class StoreSignupView(FormView):
    template_name = "store/accounts/signup.html"
    form_class = CustomerSignupForm
    success_url = reverse_lazy("store:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("store:account")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(self.request, "Регистрация завершена, вы вошли в систему.")
        return redirect(self.get_success_url())


class StoreEmployeeSignupView(FormView):
    template_name = "store/accounts/employee_signup.html"
    form_class = EmployeeSignupForm
    success_url = reverse_lazy("store:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("store:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(self.request, "Регистрация работника завершена, вы вошли в систему.")
        return redirect(self.get_success_url())


@method_decorator(require_http_methods(["POST"]), name="dispatch")
class StoreCartAddView(View):
    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(
            Product.objects.filter(is_deleted=False, is_active=True),
            pk=pk,
        )
        f = AddToCartForm(request.POST)
        if not f.is_valid():
            messages.error(request, "Некорректное количество.")
            return redirect("store:product-detail", pk=pk)
        cart_add(request, product.id, f.cleaned_data["quantity"])
        messages.success(request, "Добавлено в корзину.")
        nxt = request.POST.get("next") or reverse("store:product-detail", kwargs={"pk": pk})
        return HttpResponseRedirect(nxt)


class SupplierListView(EmployeeRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Supplier
    filterset_class = SupplierFilter
    paginate_by = 20
    template_name = "store/suppliers/supplier_list.html"
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
    template_name = "store/suppliers/supplier_detail.html"
    context_object_name = "supplier"

    def get_queryset(self):
        return _restrict_suppliers_for_limited_employee(
            self.request.user,
            Supplier.objects.filter(is_deleted=False).prefetch_related("products"),
        )


from django.db.models import Sum

class OrderListView(EmployeeRequiredMixin, StaffFilterListContextMixin, FilterView):
    model = Order
    filterset_class = OrderFilter
    paginate_by = 20
    template_name = "store/sales/sales_list.html"
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

        qs = (
            svc.orders_base_queryset()
            .annotate(
                computed_total=Sum("items__line_total")
            )
            .order_by(
                svc.order_ordering(self.request.GET.get("ordering")),
            )
        )

        return _restrict_orders_for_limited_employee(self.request.user, qs)
    

class OrderDetailView(EmployeeRequiredMixin, DetailView):
    model = Order
    template_name = "store/sales/sales_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        qs = (
            ShopStaffOrderService()
            .orders_detail_queryset()
            .annotate(
                computed_total=Sum("items__line_total")
            )
        )

        return _restrict_orders_for_limited_employee(self.request.user, qs)
