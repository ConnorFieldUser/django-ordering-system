from django.contrib import admin

from ordering_system.models import Profile, MenuItem, Order, OrderItem

# Register your models here.

admin.site.register(Profile)
admin.site.register(MenuItem)
admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)

admin.site.register(Order, OrderAdmin)
