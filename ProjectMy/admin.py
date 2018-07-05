from django.contrib import admin

from ProjectMy.models import Shop, Department, Item


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'staff_amount']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id','sphere', 'staff_amount', 'shop']

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'department', 'image']

admin.site.register(Shop, ShopAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Item, ItemAdmin)

# Register your models here.
