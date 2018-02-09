from django.conf import settings
from django.db import models
from datetime import time
from devhouse.helpers import get_attrs_n_values


class Shop(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)


class DayType(models.Model):
    name = models.CharField('name', max_length=50, null=False, unique=True)


class PeriodType(models.Model):
    name = models.CharField('name', max_length=50, null=False, unique=True)


class Schedule(models.Model):
    shop = models.ForeignKey(Shop, null=False)
    daytype = models.ForeignKey(DayType, null=False)
    periodtype = models.ForeignKey(PeriodType, null=False)
    deleted = models.BooleanField('is_deleted', null=False, default=False)
    period_start = models.TimeField('period_start', null=False, default=time(10, 0))
    period_end = models.TimeField('period_end', null=False, default=time(19, 0))
    is_working = models.BooleanField('is_working', null=False, default=True)

    class Meta:
        unique_together = ('shop', 'daytype', 'periodtype', 'deleted')

    def as_dict(self):
        return get_attrs_n_values(self)


class Shift(models.Model):
    shop = models.ForeignKey(Shop, null=False)
    opened = models.DateTimeField('ShiftOpened', null=False)
    closed = models.DateTimeField('ShiftClosed', null=True)
    now_working = models.BooleanField('now_working', null=False, default=True)

    def as_dict(self):
        return get_attrs_n_values(self)
