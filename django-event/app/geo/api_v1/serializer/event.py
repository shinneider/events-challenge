from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from app.geo import models

class State(serializers.ModelSerializer):
    initials = serializers.CharField()

    class Meta:
        model = models.State
        exclude = ('id', )

    def create(self, validated_data):
        obj, _ = models.State.objects.get_or_create(
            initials=validated_data['initials'].strip(),
            name=validated_data.get('name', '').strip()
        )
        return obj

class City(serializers.ModelSerializer):
    state = State()
    name = serializers.CharField()
    
    class Meta:
        model = models.City
        exclude = ('id', )

    def create(self, validated_data):
        obj = models.City.objects.filter(
            name=validated_data['name'].strip(),
            state=validated_data['state'].strip()
        ).first()
        
        if not obj:
            state = State(data=validated_data['state'])
            if state.is_valid():
                validated_data['state'] = state.save()

                obj, _ = models.City.objects.get_or_create(
                    name=validated_data['name'],
                    state=validated_data['state']
                )
        
            return ValueError('`state` is not valid')

        return obj
