from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from hold.models import ClimbingHold, ClimbingEquipment, Exercise, ExerciseSet, Finger, GripPosition, GripType


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


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment', 'climbing_hold')
    list_filter = ('equipment', 'climbing_hold')
    search_fields = ('name', 'equipment__name', 'climbing_hold__name')
    ordering = ('name',)


@admin.register(ExerciseSet)
class ExerciseSetAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'user', 'reps', 'hold_duration', 'effort', 'total_weight')
    list_filter = ('user', 'exercise__name')
    search_fields = ('user__username', 'user__email', 'exercise__name')
    ordering = ('-id',)

    def display_fingers(self, obj):
        left_fingers = [f.name for f in obj.exercise.finger_set.filter(hand='Left')]
        right_fingers = [f.name for f in obj.exercise.finger_set.filter(hand='Right')]
        return f"Left: {', '.join(left_fingers)}\nRight: {', '.join(right_fingers)}"

    display_fingers.short_description = _('Fingers')

    fieldsets = (
        (_('Exercise and User'), {
            'fields': ('exercise', 'user')
        }),
        (_('Exercise Details'), {
            'fields': ('reps', 'hold_duration', 'weight', 'effort')
        }),
    )


@admin.register(Finger)
class FingerAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(GripPosition)
class GripPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'fingers_used', 'finger_count', 'grip_type',)
    ordering = ('grip_type',)
    list_filter = ('grip_type', 'fingers',)
    search_fields = ('name', 'fingers__name',)
    filter_horizontal = ('fingers',)

    fieldsets = (
        (None, {'fields': ('name', 'fingers', 'grip_type', 'image',)}),
    )

    def fingers_used(self, obj):
        return ", ".join([f.name.capitalize() for f in obj.fingers.all()])

    def finger_count(self, obj):
        return obj.fingers.count()

    finger_count.short_description = 'Finger Count'
    fingers_used.short_description = "Fingers Used"
    fingers_used.admin_order_field = "fingers__name"


@admin.register(GripType)
class GripTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
