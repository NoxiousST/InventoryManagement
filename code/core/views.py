from django.db.models import Sum, ExpressionWrapper, F, FloatField, Avg, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Item, Category, Supplier

# Create your views here.
# Item Views
class ItemCreateView(CreateView):
    model = Item
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('item-list')

class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items'

# Category Views
class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('category-list')

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

# Supplier Views
class SupplierCreateView(CreateView):
    model = Supplier
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('supplier-list')

class SupplierListView(ListView):
    model = Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'

def supplier_list_json(request):
    suppliers = Supplier.objects.select_related('created_by').all()
    data = []

    for supplier in suppliers:
        data.append({
            'id': supplier.id,
            'name': supplier.name,
            'contact_info': supplier.contact_info,
            'created_by': supplier.created_by.username,
            'created_at': supplier.created_at.isoformat(),
        })

    return JsonResponse(data, safe=False)

def item_stock_summary(request):
    total_stock = Item.objects.aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

    total_stock_value = Item.objects.aggregate(
        total_value=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField()))
    )['total_value'] or 0.0

    avg_price = Item.objects.aggregate(avg=Avg('price'))['avg'] or 0.0

    return JsonResponse({
        'stok_total': total_stock,
        'total_nilai_stok': total_stock_value,
        'rata_rata_harga': round(avg_price, 2),
    })

def low_stock_items(request, threshold=5):
    items = Item.objects.filter(quantity__lt=threshold).values('id', 'name', 'quantity')

    return JsonResponse(list(items), safe=False)

def item_based_category(request, category_id):
    items = Item.objects.filter(category_id=category_id).values(
        'id', 'name', 'description', 'price', 'quantity', 'supplier__name'
    )
    return JsonResponse(list(items), safe=False)

def category_summary(request):
    data = Category.objects.annotate(
        jumlah_barang=Count('item'),
        total_nilai_stok=Sum(F('item__quantity')),
        rata_rata_harga=Avg('item__price')
    ).values(
        'id', 'name', 'jumlah_barang', 'total_nilai_stok', 'rata_rata_harga'
    )

    return JsonResponse(list(data), safe=False)