from __future__ import annotations

from django.urls import re_path

from presentation.views.store import store_views as views

app_name = "store"
urlpatterns = [
    re_path(r"^$", views.StoreHomeView.as_view(), name="home"),
    re_path(r"^about/$", views.StoreAboutView.as_view(), name="about"),

    re_path(r"^news/$", views.StoreNewsListView.as_view(), name="news-list"),
    re_path(r"^news/(?P<pk>[0-9a-f-]{36})/$", views.StoreNewsDetailView.as_view(), name="news-detail"),

    re_path(r"^faq/$", views.StoreFAQView.as_view(), name="faq"),
    re_path(r"^contacts/$", views.StoreContactsView.as_view(), name="contacts"),
    re_path(r"^privacy/$", views.StorePrivacyView.as_view(), name="privacy"),

    re_path(r"^vacancies/$", views.StoreVacancyListView.as_view(), name="vacancy-list"),
    re_path(r"^vacancies/(?P<pk>[0-9a-f-]{36})/apply/$", views.StoreVacancyApplyView.as_view(), name="vacancy-apply"),

    re_path(r"^catalog/$", views.StoreCatalogView.as_view(), name="catalog"),
    re_path(r"^catalog/(?P<pk>[0-9a-f-]{36})/$", views.StoreProductDetailView.as_view(), name="product-detail"),

    re_path(r"^cart/$", views.StoreCartView.as_view(), name="cart"),
    re_path(r"^cart/add/(?P<pk>[0-9a-f-]{36})/$", views.StoreCartAddView.as_view(), name="cart-add"),
    re_path(r"^cart/checkout/$", views.StoreCheckoutView.as_view(), name="checkout"),

    re_path(r"^account/$", views.StoreAccountView.as_view(), name="account"),
    re_path(r"^account/orders/$", views.StoreAccountOrdersView.as_view(), name="account-orders"),

    re_path(r"^reviews/$", views.StoreReviewsView.as_view(), name="reviews"),
    re_path(r"^promos/$", views.StorePromosView.as_view(), name="promos"),
    re_path(r"^pickup-points/$", views.StorePickupPointsView.as_view(), name="pickup-points"),

    re_path(r"^login/$", views.StoreLoginView.as_view(), name="login"),
    re_path(r"^logout/$", views.StoreLogoutView.as_view(), name="logout"),
    re_path(r"^signup/$", views.StoreSignupView.as_view(), name="signup"),
    re_path(r"^employee/signup/$", views.StoreEmployeeSignupView.as_view(), name="employee-signup"),

    re_path(r"^suppliers/$", views.SupplierListView.as_view(), name="supplier-list"),
    re_path(r"^suppliers/(?P<pk>[0-9a-f-]{36})/$", views.SupplierDetailView.as_view(), name="supplier-detail"),

    re_path(r"^orders/$", views.OrderListView.as_view(), name="order-list"),
    re_path(r"^orders/(?P<pk>[0-9a-f-]{36})/$", views.OrderDetailView.as_view(), name="order-detail"),
]
