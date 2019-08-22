from django.urls import path
from .views import ListRidesView, FileUploadView, FlushDatabaseView


urlpatterns = [
    path('list/', ListRidesView.as_view(), name="list-all-rides"),
    path('upload/', FileUploadView.as_view(), name='upload-file'),
    path('flushdb/', FlushDatabaseView.as_view(), name='flush-db'),
]