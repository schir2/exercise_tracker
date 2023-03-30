from django.contrib import admin
from django.utils.html import format_html

from hold.models import ClimbingHold, ClimbingEquipment, Exercise, ExerciseSet, Finger, ExerciseHandConfiguration, \
    ExerciseSetHandConfiguration


class ClimbingHoldInline(admin.TabularInline):  # You can also use admin.StackedInline for a different layout
    model = ClimbingHold
    extra = 1  # Defines the number of empty forms to display


@admin.register(ClimbingEquipment)
class ClimbingEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment_type', 'manufacturer', 'image_thumbnail')
    readonly_fields = ('image_thumbnail',)
    search_fields = ('name', 'manufacturer')
    list_filter = ('equipment_type',)
    inlines = [ClimbingHoldInline]

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"

    image_thumbnail.short_description = 'Image'


@admin.register(ClimbingHold)
class ClimbingHoldAdmin(admin.ModelAdmin):
    list_display = ('name', 'hold_type', 'size', 'depth', 'angle', 'climbing_equipment')
    search_fields = ('name', 'climbing_equipment__name')
    list_filter = ('hold_type',)


class ExerciseHandConfigurationInline(admin.TabularInline):
    model = ExerciseHandConfiguration
    extra = 1
    min_num = 1
    max_num = 2


class ExerciseSetHandConfigurationInline(admin.TabularInline):
    model = ExerciseSetHandConfiguration
    extra = 0


class ExerciseAdmin(admin.ModelAdmin):
    inlines = [ExerciseHandConfigurationInline]


class ExerciseSetAdmin(admin.ModelAdmin):
    inlines = [ExerciseSetHandConfigurationInline]


class FingerAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseSet, ExerciseSetAdmin)
admin.site.register(Finger, FingerAdmin)
