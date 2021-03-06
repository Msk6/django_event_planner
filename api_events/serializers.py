from rest_framework import serializers
from events.models import Event, Booking
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(new_user.password)
        new_user.save()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class EventListSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()
    owner = UserSerializer()
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'datetime', 'available_seats', 'owner']
    
    def get_available_seats(self, obj):
        return obj.seats - obj.reserved_seats


class BookingListSerializer(serializers.ModelSerializer):
    event = EventListSerializer()
    user = UserSerializer()
    class Meta:
        model = Booking
        fields = ['event', 'user', 'seats']


class EventGuestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Booking
        fields = ['user', 'seats']


class EventBookingsListSerializer(serializers.ModelSerializer):
    event_bookings = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['event', 'event_bookings',]
    
    def get_event_bookings(self, obj):
        return EventGuestSerializer(obj.bookings.all(), many=True).data

    def get_event(self, obj):
        return EventListSerializer(obj).data


class AddUpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['owner', 'slug','datetime']


class BookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['seats']
    

    
