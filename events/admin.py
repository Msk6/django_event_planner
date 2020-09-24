from django.contrib import admin
from .models import Event, Booking, Comment, Connection


admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(Comment)
admin.site.register(Connection)