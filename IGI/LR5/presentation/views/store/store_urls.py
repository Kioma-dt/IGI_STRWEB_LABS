from __future__ import annotations

from django.urls import path

from presentation.views.store import store_views as views

app_name = "store"

urlpatterns = [
    path("", views.StoreHomeView.as_view(), name="home"),
    path("about/", views.StoreAboutView.as_view(), name="about"),
    path("news/", views.StoreNewsListView.as_view(), name="news-list"),
    path("news/<uuid:pk>/", views.StoreNewsDetailView.as_view(), name="news-detail"),
    path("faq/", views.StoreFAQView.as_view(), name="faq"),
    path("contacts/", views.StoreContactsView.as_view(), name="contacts"),
    path("privacy/", views.StorePrivacyView.as_view(), name="privacy"),
    path("vacancies/", views.StoreVacancyListView.as_view(), name="vacancy-list"),
    path(
        "vacancies/<uuid:pk>/apply/",
        views.StoreVacancyApplyView.as_view(),
        name="vacancy-apply",
    ),
    path("catalog/", views.StoreCatalogView.as_view(), name="catalog"),
    path(
        "catalog/<uuid:pk>/",
        views.StoreProductDetailView.as_view(),
        name="product-detail",
    ),
    path("cart/", views.StoreCartView.as_view(), name="cart"),
    path("cart/add/<uuid:pk>/", views.StoreCartAddView.as_view(), name="cart-add"),
    path("cart/checkout/", views.StoreCheckoutView.as_view(), name="checkout"),
    path("account/", views.StoreAccountView.as_view(), name="account"),
    path("account/orders/", views.StoreAccountOrdersView.as_view(), name="account-orders"),
    path("reviews/", views.StoreReviewsView.as_view(), name="reviews"),
    path("promos/", views.StorePromosView.as_view(), name="promos"),
    path("pickup-points/", views.StorePickupPointsView.as_view(), name="pickup-points"),
    path("login/", views.StoreLoginView.as_view(), name="login"),
    path("logout/", views.StoreLogoutView.as_view(), name="logout"),
    path("signup/", views.StoreSignupView.as_view(), name="signup"),
    path("employee/signup/", views.StoreEmployeeSignupView.as_view(), name="employee-signup"),

    path("suppliers/", views.SupplierListView.as_view(), name="supplier-list"),
    path("suppliers/<uuid:pk>/", views.SupplierDetailView.as_view(), name="supplier-detail"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/<uuid:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
]
