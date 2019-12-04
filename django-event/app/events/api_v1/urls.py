from django.urls import path

from app.events.api_v1 import views

urlpatterns = [
    path('events', views.EventsListView.as_view()),
    path('events/<int:pk>', views.EventRetrieveView.as_view()),
    path('events/metrics', views.MetricsView.as_view()),
]
