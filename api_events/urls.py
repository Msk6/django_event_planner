from django.urls import path
from api_events import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='api-login'),
    path('signup/', views.Register.as_view(), name='api-signup'),

    path('event/list/', views.EventList.as_view(), name='api-event-list'),
    path('event/list/organizer/', views.OrganizerEvents.as_view(), name='api-organizer-event-list'),
    path('event/bookings/list/user/', views.UserBookedEvents.as_view(), name='api-user-bookings'),
    path('event/<str:event_slug>/bookings/list/', views.BookingsForEvent.as_view(), name='api-event-bookings'),
    
    path('event/add/', views.AddEvent.as_view(), name='api-add-event'),
    path('event/<str:event_slug>/update/', views.UpdateEvent.as_view(), name='api-update-event'),
    path('event/<str:event_slug>/book/', views.BookEvent.as_view(), name='api-book-event'),
]