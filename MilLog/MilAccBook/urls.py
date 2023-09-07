from django.urls import path
from django.views.generic import DetailView, ListView
from .models import ProductVariant
from .views import ProductsView, ProductVariantView

urlpatterns = [
    path("product/", ProductsView.as_view()),
    path("product_variant/", ListView.as_view(model=ProductVariant)),
    path("product_variant/<int:pk>/", DetailView.as_view(model=ProductVariant)),
    path("pv_page/<int:pv_id>", ProductVariantView.pv_page),
]
