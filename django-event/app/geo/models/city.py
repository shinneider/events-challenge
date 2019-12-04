from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    state = models.ForeignKey('geo.state', on_delete=models.CASCADE, verbose_name=_("state"))
    name = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("name"))

    class Meta:
        db_table = "geo_city"

    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.name, self.state.initials)

