from django.urls import path, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .models import Document, DocumentProduct, JournalLine, OperationSubline, Peer, Product, ProductGroup, ProductVariant
from .views import AssetGroupView, AssetView, DocumentCreateView, ProductsView, ProductVariantView

urlpatterns = [
    path("document/", ListView.as_view(model=Document), name='documents'),
    path("document/add/", DocumentCreateView.as_view(), name='document-create'),
    #path("document/<int:pk>/", UpdateView.as_view(model=Document)),
    path('document/<int:pk>/', DetailView.as_view(model=Document), name='document-detail'),
    path("documentproduct/", ListView.as_view(model=DocumentProduct), name='documentproducts'),
    path("documentproduct/add/", CreateView.as_view(model=DocumentProduct, fields=['document', 'product_variant', 'total_q', 'sort1_q', 'sort2_q', 'sort3_q', 'sort4_q', 'sort5_q'], success_url=reverse_lazy('documentproducts')), name='documentproduct-create'),
    path("journalline/", ListView.as_view(model=JournalLine), name='journallines'),
    path("journalline/add/", CreateView.as_view(model=JournalLine, fields=['record_date', 'document_product'], success_url=reverse_lazy('journallines')), name='operationsubline-create'),
    path("operationsubline/", ListView.as_view(model=OperationSubline), name='operationsublines'),
    path("operationsubline/add/", CreateView.as_view(model=OperationSubline, fields=['operation', 'peer', 'document_product', 'total_q', 'sort1_q', 'sort2_q', 'sort3_q', 'sort4_q', 'sort5_q'], success_url=reverse_lazy('operationsublines')), name='operationsubline-create'),
    path("peer/", ListView.as_view(model=Peer), name='peers'),
    path("peer/add/", CreateView.as_view(model=Peer, fields=['name'], success_url=reverse_lazy('peers')), name='peer-create'),
    path("product/", ProductsView.as_view(), name='products'),
    path("product/add/", CreateView.as_view(model=Product, fields=['name', 'has_sort', 'uom', 'group'], success_url=reverse_lazy('products')), name='product-create'),
    path("product_variant/", ListView.as_view(model=ProductVariant), name='productvariants'),
    path("product_variant/<int:pk>/", DetailView.as_view(model=ProductVariant)),
    path("product_variant/add/", CreateView.as_view(model=ProductVariant, fields=['product', 'price'], success_url=reverse_lazy('productvariants')), name='productvariant-create'),
    path("pv_page/<int:pv_id>", ProductVariantView.pv_page),
    path("asset", AssetView.asset_page),
    path("productgroup/", ListView.as_view(model=ProductGroup), name='productgroups'),
    path("productgroup/add/", CreateView.as_view(model=ProductGroup, fields=['name', 'parent'], success_url=reverse_lazy('productgroups')), name='productgroup-create'),
    path("assetgroup", AssetGroupView.asset_page),
]
