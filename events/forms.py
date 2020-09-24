from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking, Comment

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats']


class AddUpdateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner', 'slug',]


class PersonalInfoUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

