from django.urls import path

from app.events.api_v1 import views

urlpatterns = [
    path('events', views.EventsList.as_view()),
    path('events/<int:pk>', views.EventRetrieve.as_view()),
]
