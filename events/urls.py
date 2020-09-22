from django.urls import path
from events import views

urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    
    path('event/list/', views.event_list, name='event-list'),# any and organizer only #
    path('event/<str:event_slug>/detail/', views.event_detail, name='event-detail'),# any and organizer only #
    path('event/<str:event_slug>/booking/', views.event_booking, name='event-booking'),# user #

    path('event/bookings/list/user/', views.view_bookings, name='bookings-list-user'),# user #

    path('event/add/', views.add_event, name='add-event'),# user #
    path('event/<str:event_slug>/update/', views.update_event, name='update-event'),# organizer #
]