from django.urls import path
from .views import ListRidesView


urlpatterns = [
    path('list/', ListRidesView.as_view(), name="list-all-rides"),
]