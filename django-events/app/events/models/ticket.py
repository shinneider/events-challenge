from django.db import models
from django.utils.translation import ugettext_lazy as _


class Ticket(models.Model):
    event = models.ForeignKey('events.event', on_delete=models.CASCADE, verbose_name=_("city"))
    name = models.CharField(max_length=100, verbose_name=_("name"))
    value = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("value"))

    class Meta:
        db_table = "events_ticket"

    def __str__(self):  # pragma: no cover
        return self.name
