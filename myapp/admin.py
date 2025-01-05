from django.contrib import admin
from .models import CustomUser, Category, Product, ProductImage, Cart, CartItem, Wishlist, Order, OrderItem, ShippingAddress

# Custom admin interface for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Custom admin interface for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

# Custom admin interface for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

# Custom admin interface for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'status', 'product_price')
    search_fields = ('customer_email', 'id')
    list_filter = ('status',)

# Register models with admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
