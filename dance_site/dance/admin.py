from django.contrib import admin
from .models import DanceGroup, DanceStyle, Dancer, Performance

@admin.register(DanceGroup)
class DanceGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('name', 'city')
    list_filter = ('city',)

@admin.register(DanceStyle)
class DanceStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Dancer)
class DancerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'group')
    search_fields = ('name',)
    list_filter = ('group',)

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'style', 'date', 'location')
    search_fields = ('location',)
    list_filter = ('date', 'group', 'style')
