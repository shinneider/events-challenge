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
        by_city = models.Event.objects.values(
            'city__name',
            'city__state__initials'
        ).annotate(
            total_events = Count('city'),
        ).order_by()

        by_state = models.Event.objects.values(
            'city__state__initials'
        ).annotate(
            total_events = Count('city__state'),
        ).order_by()

        average = (models.Event.objects.aggregate(Count('ticket'))['ticket__count'] /
                   models.Event.objects.count())

        biggest_price = models.Event.objects.filter(
            ticket__isnull=False
        ).values(
            'id', 'name', 'event_url'
        ).annotate(
            ticket_biggest_price = Max('ticket__value'),
        ).order_by('-ticket_biggest_price').first()

        events_by_day_week = 'not implemented'

        return Response({
            'events_by': {
                'city': by_city,
                'state': by_state
            },
            'biggest_price': biggest_price,
            'events_ticket_average': average,
            'events_by_day_week': events_by_day_week
        })
