from django.urls import path
from .views import ListRidesView, FileUploadView, FlushDatabaseView, BulkFileUploadView


urlpatterns = [
    path('list/', ListRidesView.as_view(), name="list-all-rides"),
    path('upload/', FileUploadView.as_view(), name='upload-file'),
    path('bulk/', BulkFileUploadView.as_view(), name='upload-bulk-create'),
    path('flushdb/', FlushDatabaseView.as_view(), name='flush-db'),
]