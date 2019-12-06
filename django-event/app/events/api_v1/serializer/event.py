from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from app.geo.api_v1.serializer.event import City
from app.events import models


class TicketCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        exclude = ('id', )

class TicketView(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        exclude = ('id', 'event', )

class Event(serializers.ModelSerializer):
    city = City(required=False)
    tickets = TicketView(source='ticket_set', many=True, required=False)
    
    class Meta:
        model = models.Event
        fields = ('__all__')

    def validate(self, data):
        if not (data.get('event_online', None) or data.get('city', None)):
            raise serializers.ValidationError({
                'event_online': [_('This field or `city` field is required.')],
                'city': ['This field or `event_online` field is required.']
            })

        return data

    def create(self, validated_data):
        event = models.Event.objects.filter(
            event_url=validated_data['event_url']
        ).first()
        if event:
            return event

        ticket = validated_data.pop('ticket_set', None)

        if validated_data.get('city', None):
            city = City(data=validated_data['city'])
            if not city.is_valid():
                raise ValueError('`city` is not valid')
            
            validated_data['city'] = city.save()

        obj = super().create(validated_data)
        self.create_ticket(ticket, obj)
        return obj
    
    def create_ticket(self, ticket, event):
        if not ticket:
            return
        
        for item in ticket:
            item.update({'event': event.pk})

        ticket = TicketCreate(data=ticket, many=True)
        if not ticket.is_valid():
            raise ValueError(ticket.errors)
        
        ticket.save()
