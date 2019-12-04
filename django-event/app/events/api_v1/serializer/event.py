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
    city = City()
    ticket = TicketView(source='ticket_set', many=True, required=False)
    
    class Meta:
        model = models.Event
        fields = ('__all__')

    def create(self, validated_data):
        ticket = validated_data.pop('ticket_set', None)

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
