from app.events import models
from app.shared.logger import Logger
from app.shared.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, F, Max, Avg
from django.db.models.functions import Upper

class MetricsView(APIView):
    queryset = models.Event.objects.all()
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        return Response({
            'events_by': {
                'online': self.get_events_online(),
                'city': self.get_events_by_city(),
                'state': self.get_events_by_state(),
            },
            'biggest_price': self.get_events_biggest_price(),
            'events_ticket_average': self.get_events_average(),
            'events_by_day_week': 'not implemented',
            'events_with_facebook_url': self.get_events_with_facebook_url()
        })

    def get_events_online(self):
        return models.Event.objects.filter(event_url=True).count()

    def get_events_by_city(self):
        return models.Event.objects.filter(
            city__isnull=False
        ).values(
            'city__name', 'city__state__initials'
        ).annotate(
            city_name=F('city__name'),
            state_name=F('city__state__initials'),
            total_events = Count('city'),
        ).values('city_name', 'state_name', 'total_events').order_by()

    def get_events_by_state(self):
        return models.Event.objects.filter(
            city__isnull=False
        ).values('city__state__initials').annotate(
            state_name=F('city__state__initials'),
            total_events = Count('city__state'),
        ).values('state_name','total_events').order_by()

    def get_events_average(self):
        return (models.Event.objects.aggregate(Count('ticket'))['ticket__count'] /
                models.Event.objects.count())

    def get_events_biggest_price(self):
        return models.Event.objects.filter(
            ticket__isnull=False
        ).values(
            'id', 'name', 'event_url'
        ).annotate(
            ticket_biggest_price = Max('ticket__value'),
        ).order_by('-ticket_biggest_price').first()

    def get_events_with_facebook_url(self):
        return models.Event.objects.filter(
            description__regex=r'https://www.facebook.com/events/.*/'
        ).values(
            'id', 'name', 'event_url'
        )
