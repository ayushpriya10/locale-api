from django.urls import path
from .views import ListRidesView, FlushDatabaseView, TaskStatus, AsyncFileHandler, RideDetails


urlpatterns = [
    path('list/', ListRidesView.as_view(), name="list-all-rides"),
    path('flushdb/', FlushDatabaseView.as_view(), name='flush-db'),
    path('task_status/', TaskStatus.as_view(), name='async-task-status'),
    path('asyncfile/', AsyncFileHandler.as_view(), name='async-file-handler'),
    path('ride_details/', RideDetails.as_view(), name='ride-details'),
]