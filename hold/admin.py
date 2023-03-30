from django.contrib import admin

from hold.models import ClimbingHold, ClimbingEquipment


class ClimbingHoldInline(admin.TabularInline):  # You can also use admin.StackedInline for a different layout
    model = ClimbingHold
    extra = 1  # Defines the number of empty forms to display


@admin.register(ClimbingEquipment)
class ClimbingEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment_type', 'manufacturer')
    search_fields = ('name', 'manufacturer')
    list_filter = ('equipment_type',)
    inlines = [ClimbingHoldInline]


@admin.register(ClimbingHold)
class ClimbingHoldAdmin(admin.ModelAdmin):
    list_display = ('name', 'hold_type', 'size', 'depth', 'angle', 'climbing_equipment')
    search_fields = ('name', 'climbing_equipment__name')
    list_filter = ('hold_type',)
