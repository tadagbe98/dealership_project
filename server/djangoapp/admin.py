from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_of_origin', 'founded_year')
    search_fields = ('name',)
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'car_type', 'year', 'dealer_id')
    list_filter = ('car_type', 'year', 'car_make')
    search_fields = ('name', 'car_make__name')
