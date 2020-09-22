from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
    )
from .serializers import (
    RegisterSerializer, EventListSerializer, BookingListSerializer,
    EventBookingsListSerializer, AddUpdateEventSerializer, BookEventSerializer
    )
from events.models import Event, Booking 
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class EventList(ListAPIView):
    queryset = Event.objects.filter(datetime__gte=datetime.today()).order_by('-datetime')
    serializer_class = EventListSerializer


class OrganizerEvents(ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.event_set.all().order_by('-datetime')


class BookingsForEvent(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventBookingsListSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'event_slug'
    permission_classes = [IsAuthenticated]


class UserBookedEvents(ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.bookings.all().order_by('-event__datetime')


class AddEvent(CreateAPIView):
    serializer_class = AddUpdateEventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class UpdateEvent(RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = AddUpdateEventSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'event_slug'
    permission_classes = [IsAuthenticated, IsOwner] #IsOwner


class BookEvent(CreateAPIView):
    serializer_class = BookEventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event = Event.objects.get(slug=self.kwargs['event_slug'])
        return serializer.save(user=self.request.user, event=event)




