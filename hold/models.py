from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_measurement.models import MeasurementField
from measurement.measures import Distance, Weight

from user.models import UserProfile

LENGTH_UNITS = [
    ('mm', _('Millimeters')),
    ('cm', _('Centimeters')),
    ('m', _('Meters')),
    ('inch', _('Inches')),
    ('ft', _('Feet')),
]

WEIGHT_UNITS = [
    ('lb', _('Pounds')),
    ('kg', _('Kilograms')),
]


class ClimbingEquipment(models.Model):
    EQUIPMENT_TYPES = (
        ('HB', _('Hangboard')),
        ('PB', _('Pinch Block')),
        ('CB', _('Campus Board')),
        ('TB', _('Training Board')),
    )

    name = models.CharField(_('name'), max_length=100)
    equipment_type = models.CharField(_('equipment type'), max_length=2, choices=EQUIPMENT_TYPES)
    manufacturer = models.CharField(_('manufacturer'), max_length=100, blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='climbing_equipment/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('climbing equipment')
        verbose_name_plural = _('climbing equipment')


class ClimbingHold(models.Model):
    HOLD_TYPES = (
        ('JG', _('Jug')),
        ('SL', _('Sloper')),
        ('CR', _('Crimp')),
        ('PC', _('Pinch')),
        ('PK', _('Pocket')),
        ('SP', _('Sidepull')),
        ('GT', _('Gaston')),
        ('UC', _('Undercling')),
        # Add more hold types if needed
    )

    name = models.CharField(_('name'), max_length=100)
    hold_type = models.CharField(_('hold type'), max_length=2, choices=HOLD_TYPES)
    size = MeasurementField(_('size'), unit_choices=LENGTH_UNITS, measurement=Distance, blank=True, null=True,
                            help_text=_("Size of the edge, pocket, or other dimensions as applicable"))
    depth = MeasurementField(_('depth'), measurement=Distance, unit_choices=LENGTH_UNITS, blank=True, null=True,
                             help_text=_("Depth of the hold, if applicable"))
    angle = models.IntegerField(_('angle'), blank=True, null=True, help_text=_("Angle of the hold, if applicable"))
    climbing_equipment = models.ForeignKey(ClimbingEquipment, on_delete=models.CASCADE,
                                           verbose_name=_('climbing equipment'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('climbing hold')
        verbose_name_plural = _('climbing holds')


class Finger(models.Model):
    FINGER_CHOICES = [
        ('thumb', _('Thumb')),
        ('index', _('Index')),
        ('middle', _('Middle')),
        ('ring', _('Ring')),
        ('pinky', _('Pinky')),
    ]
    name = models.CharField(max_length=10, choices=FINGER_CHOICES)

    def __str__(self):
        return self.name


HAND_CHOICES = [
    ('Left', 'Left'),
    ('Right', 'Right'),
    ('Both', 'Both'),
]


class ExerciseSetHandConfiguration(models.Model):
    exercise_set = models.ForeignKey('ExerciseSet', on_delete=models.CASCADE)
    hand = models.CharField(max_length=10, choices=HAND_CHOICES)
    fingers = models.ManyToManyField(Finger)

    class Meta:
        verbose_name_plural = 'Exercise Set Hand Configurations'

    def __str__(self):
        return f"{self.hand} - {', '.join([str(finger) for finger in self.fingers.all()])}"

    def save(self, *args, **kwargs):
        if self.exercise_set.exercisesethandconfiguration_set.count() >= 2:
            raise ValidationError("You can associate at most two hands with an ExerciseSet.")
        super().save(*args, **kwargs)


class ExerciseHandConfiguration(models.Model):
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    hand = models.CharField(max_length=10, choices=HAND_CHOICES)
    fingers = models.ManyToManyField('Finger')

    def __str__(self):
        return f"{self.hand} - {', '.join([str(finger) for finger in self.fingers.all()])}"

    def save(self, *args, **kwargs):
        if self.exercise.exercisehandconfiguration_set.count() >= 2:
            raise ValidationError("You can associate at most two hands with an Exercise.")
        super().save(*args, **kwargs)


def copy_hand_configurations_to_exercise_set(exercise, exercise_set):
    for exercise_hand_config in exercise.exercisehandconfiguration_set.all():
        hand_config = ExerciseSetHandConfiguration(exercise_set=exercise_set, hand=exercise_hand_config.hand)
        hand_config.save()
        hand_config.fingers.set(exercise_hand_config.fingers.all())


class ExerciseSetManager(models.Manager):
    def create(self, *args, **kwargs):
        exercise = kwargs['exercise']
        exercise_set = super().create(*args, **kwargs)
        copy_hand_configurations_to_exercise_set(exercise, exercise_set)
        return exercise_set


class Exercise(models.Model):
    name = models.CharField(_('name'), max_length=100)
    uses_bodyweight = models.BooleanField(_('uses bodyweight'), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Exercise')
        verbose_name_plural = _('Exercise')


class ExerciseSet(models.Model):
    """
    A model representing a set of exercises, which includes information on the exercise, the user performing the exercise,
    the hold duration, weight, number of repetitions, and effort rating.
    """
    EFFORT_CHOICES = [
        ('1', _('Very easy')),
        ('2', _('Easy')),
        ('3', _('Moderate')),
        ('4', _('Hard')),
        ('5', _('Very hard')),
    ]

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    hold_duration = models.FloatField(_('hold duration'), blank=True, null=True, help_text=_('in seconds'))
    weight = MeasurementField(_('weight'), measurement=Weight, unit_choices=WEIGHT_UNITS)
    reps = models.PositiveIntegerField(_('reps'), default=1)
    effort = models.CharField(_('effort'), max_length=10, choices=EFFORT_CHOICES, default='M')

    objects = ExerciseSetManager()

    def total_weight(self):
        weight = self.weight
        if self.exercise.uses_bodyweight:
            weight += self.user.userprofile.body_weight
        return weight

    def __str__(self):
        rep_str = f"x{self.reps}" if self.reps > 1 else ""
        hold_duration_str = f" ({self.hold_duration}s)" if self.hold_duration else ""
        weight_str = f" ({self.total_weight()})" if self.total_weight() else ""
        return f"{self.exercise.name}{rep_str}{hold_duration_str}{weight_str} - {self.effort}"
