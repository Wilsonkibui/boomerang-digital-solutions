from django.contrib import admin
from .models import Category, Brand, Product, Order, OrderItem, SiteSetting

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_status', 'category', 'brand', 'is_featured')
    list_filter = ('stock_status', 'is_featured', 'category', 'brand')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock_status', 'is_featured')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('subtotal',)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('setting_key', 'setting_value', 'updated_at')
