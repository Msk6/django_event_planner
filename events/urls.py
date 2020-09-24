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
    path('event/<str:organizer_username>/organizer/list/', views.organizer_events, name='organizer-event-list'),

    path('event/add/', views.add_event, name='add-event'),# user #
    path('event/<str:event_slug>/update/', views.update_event, name='update-event'),# organizer #

    #path('event/user/info/', views.personal_info, name='view-personal-info'),
    path('event/<str:user_username>/info/', views.personal_info_update, name='update-view-personal-info'),
    path('event/<str:user_username>/password/update/', views.change_pssword, name='update-password'),

    path('follow/<str:user_username>/', views.follow, name='follow'),
    path('unfollow/<str:user_username>/', views.unfollow, name='unfollow'),
]