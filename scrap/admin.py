from django.contrib import admin
from .models import Client, Car
# Register your models here.


def run_category_script(modeladmin, request, queryset):
    for client in queryset:
        client.run_script()
    modeladmin.message_user(request, f'done')


run_category_script.short_description = "Run Script"


class ClientAdmin(admin.ModelAdmin):
    list_display = ('client',)
    actions = [run_category_script]


class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'year', 'price',
                    'mile', 'body_health', 'engine_status', 'source')


admin.site.register(Client, ClientAdmin)
admin.site.register(Car, CarAdmin)
