"""
URL configuration for simpleim project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import (
    ItemCreateView, ItemListView,
    CategoryCreateView, CategoryListView,
    SupplierCreateView, SupplierListView,
)

from core.views import supplier_list_json, item_stock_summary, low_stock_items, item_based_category, category_summary

urlpatterns = [
    path('admin/', admin.site.urls),

    # Item
    path('items/create/', ItemCreateView.as_view(), name='item-create'),
    path('items/', ItemListView.as_view(), name='item-list'),

    # Category
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # Supplier
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier-create'),
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),

    path('api/suppliers/', supplier_list_json, name='supplier-list-json'),

    path('api/items/summary/', item_stock_summary, name='item-stock-summary'),
    path('api/items/low-stock/', low_stock_items, name='low-stock-items'),

    path('api/categories/<int:category_id>/', item_based_category, name='laporan-kategori'),
    path('api/categories/summary/', category_summary, name='ringkasan-kategori'),
]
