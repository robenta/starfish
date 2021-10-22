from django.contrib import admin
from . models import Category, Product, Carousel, ShopCart, Payment
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'image')

#django always adds an 'id' so you must always add it.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'price', 'max','image', 'description', 'featured', 'latest', 'available', 'min')

class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'basket_no', 'quantity', 'paid_order')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'basket_no', 'pay_code', 'paid_order', 'first_name', 'last_name', 'phone', 'address', 'city', 'state')    
    
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin) 
admin.site.register(Carousel,CarouselAdmin)     
admin.site.register(ShopCart,ShopCartAdmin)   
admin.site.register(Payment,PaymentAdmin)           