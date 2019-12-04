from django.db import models
from django.utils.translation import ugettext_lazy as _


class State(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("name"))
    initials = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("initials"))

    class Meta:
        db_table = "geo_state"

    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.name, self.initials)

