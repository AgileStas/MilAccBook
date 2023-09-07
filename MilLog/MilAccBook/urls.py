from django.urls import path
from django.views.generic import ListView
from .models import ProductVariant
from .views import ProductsView

urlpatterns = [
    path("product/", ProductsView.as_view()),
    path("product_variant/", ListView.as_view(model=ProductVariant)),
]