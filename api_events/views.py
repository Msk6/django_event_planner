from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import RegisterSerializer, EventListSerializer, BookingListSerializer
from events.models import Event, Booking 
from datetime import datetime
from rest_framework.permissions import IsAuthenticated


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class EventList(ListAPIView):
    queryset = Event.objects.filter(datetime__gte=datetime.today()).order_by('-datetime')
    serializer_class = EventListSerializer


class OrganizerEvents(ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.event_set.all()


class UserBookedEvents(ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.bookings.all()


