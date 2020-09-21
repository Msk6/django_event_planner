from django.urls import path
from events import views

urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    
    path('event/list/', views.event_list, name='event-list'),
    path('event/<str:event_slug>/detail/', views.event_detail, name='event-detail'),
    path('event/<str:event_slug>/booking/', views.event_booking, name='event-booking'),

    path('event/bookings/user/', views.view_bookings, name='view-bookings'),

    path('event/add/', views.add_event, name='add-event'),
    path('event/<str:event_slug>/update/', views.update_event, name='update-event'),
]