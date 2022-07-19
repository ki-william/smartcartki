from django.contrib import admin
from .models import * 

class OrderAdminInline(admin.StackedInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderAdminInline, )
admin.site.register(Order, OrderAdmin)

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
admin.site.register(Rate)
admin.site.register(Usedtransactions)





