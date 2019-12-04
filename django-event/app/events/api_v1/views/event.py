from app.events import models
from app.events.api_v1 import serializer
from app.shared.logger import Logger
from app.shared.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import generics


class EventsListView(generics.ListCreateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializer.Event
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request, *args, **kwargs):
        Logger.info('Event create request', request=request)
        return super().post(request, *args, **kwargs)


class EventRetrieveView(generics.RetrieveAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializer.Event
    permission_classes = (AllowAny, )

    def get_object(self):
        origin = self.request.query_params.get('origin', 'internal')

        if origin == 'internal':
            return super().get_object()

        elif origin == 'sympla':
            return self.queryset.filter(
                event_url__endswith='__{}'.format(self.kwargs['pk'])
            ).first()

        return None