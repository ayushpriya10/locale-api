from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ride
from .serializers import RidesSerializer


class ListRidesView(APIView):

    def get(self, request):
        rides = Ride.objects.all()
        serializer = RidesSerializer(rides, many=True)

        return Response({"rides": serializer.data})


