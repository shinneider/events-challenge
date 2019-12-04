from app.accounts import models
from app.accounts.api_v1 import serializer
from app.shared.logger import Logger
from app.shared.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import generics


class EventsList(generics.ListCreateAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializer.Event
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request, *args, **kwargs):
        Logger.info('Event create request', request=request)
        return super().post(request, *args, **kwargs)


class EventRetrieve(generics.RetrieveAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializer.Event
    permission_classes = (AllowAny, )
