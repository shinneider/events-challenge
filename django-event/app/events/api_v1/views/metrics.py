from app.events import models
from app.shared.logger import Logger
from app.shared.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response


class MetricsView(APIView):
    queryset = models.Event.objects.all()
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        Logger.info('Get metrics', request=request)
        return Response({})
