from django.db import models
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    city = models.ForeignKey('geo.city', on_delete=models.CASCADE, verbose_name=_("city"))
    name = models.TextField(verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    start_at = models.DateTimeField(verbose_name=_("start at"))
    finish_at = models.DateTimeField(verbose_name=_("finish at"))

    class Meta:
        db_table = "events_event"

    def __str__(self):  # pragma: no cover
        return self.name
