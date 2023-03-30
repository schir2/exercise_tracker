from django.db import models
from django.utils.translation import gettext_lazy as _


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
    size = models.FloatField(_('size'), help_text=_("Size of the edge, pocket, or other dimensions as applicable"))
    depth = models.FloatField(_('depth'), help_text=_("Depth of the hold, if applicable"))
    angle = models.FloatField(_('angle'), blank=True, null=True, help_text=_("Angle of the hold, if applicable"))
    climbing_equipment = models.ForeignKey(ClimbingEquipment, on_delete=models.CASCADE,
                                           verbose_name=_('climbing equipment'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('climbing hold')
        verbose_name_plural = _('climbing holds')
