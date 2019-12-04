from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from app.events import models


class Event(serializers.ModelSerializer):
    class Meta:
        model = models.Event

