from django.urls import path
from api_events import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='api-login'),
    path('signup/', views.Register.as_view(), name='api-signup'),

    path('event/list/', views.EventList.as_view(), name='api-event-list'),
    path('event/list/organizer', views.OrganizerEvents.as_view(), name='api-organizer-event-list'),
    path('event/bookings/list', views.UserBookedEvents.as_view(), name='api-user-bookings'),
]