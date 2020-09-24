from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import (
    UserSignup, UserLogin, EventBookingForm, AddUpdateEventForm,
     PersonalInfoUpdate, ChangePasswordForm, CommentForm
     )
from .models import Event, Booking, Comment, Connection
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('event-list')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("event-list")


# ----- Any user -----

def event_list(request):
    events = Event.objects.filter(datetime__gte=datetime.today()).order_by('datetime')

    # permission organizer
    # in HTML (only authenticated)

    query = request.GET.get('search')
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(owner__username__icontains=query)
            ).distinct()
    context = {
        'events': events,
    }
    return render(request, 'list_test.html', context)


def event_detail(request, event_slug):
    event = Event.objects.get(slug=event_slug)
    comments = event.comments.all()
    form = CommentForm()

    if request.user.is_authenticated: 
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment_obj = form.save(commit=False)
                comment_obj.user = request.user
                comment_obj.event = event
                comment_obj.save()
                messages.success(request, "Added comment successfully")
                return redirect('event-detail', event_slug=event.slug)
            
    # permission (only organizer)
    # in HTML 

    context = {
        'event': event,
        'comments': comments,
        'form':form,
    }
    return render(request, 'detail_test.html', context)
 
# ----- All Registered user -----
#book_event
def event_booking(request, event_slug):
    # permission
    if not request.user.is_authenticated:
        return redirect('login')

    form = EventBookingForm()
    event = Event.objects.get(slug=event_slug)
    if request.method == "POST":
        form = EventBookingForm(request.POST)
        if form.is_valid():
            # Check seats availability
            if form.cleaned_data['seats'] + event.reserved_seats > event.seats:
                messages.warning(request, "No enough seats")
                return redirect('event-booking', event_slug)

            booking_obj = form.save(commit=False)
            booking_obj.user = request.user
            booking_obj.event = event
            booking_obj.save()
            return redirect('event-list')

    context = {
        'form':form,
        'event':event,
    }
    return render(request, 'event_booking_test.html', context)

#user_view_bookings
def view_bookings(request):
    # permission
    if not request.user.is_authenticated:
        return redirect('login')

    bookings = Booking.objects.filter(user=request.user).order_by('-event__datetime')
    if request.GET.get('past'):
        bookings = Booking.objects.filter(user=request.user, event__datetime__lte=datetime.today()).order_by('-event__datetime')
    if request.GET.get('all'):
        bookings = Booking.objects.filter(user=request.user).order_by('-event__datetime')
    if request.GET.get('upcoming'):
        bookings = Booking.objects.filter(user=request.user, event__datetime__gt=datetime.today()).order_by('-event__datetime')
    
    context = {
        'bookings':bookings,
    }
    return render(request, 'view_bookings_test.html', context)

def delete_comment(request, comment_id):
    pass

def update_comment(request, comment_id):
    pass

# ----- Organizer -----

def add_event(request):
    # permission
    if not request.user.is_authenticated:
        return redirect('login')

    form = AddUpdateEventForm()
    if request.method == "POST":
        form = AddUpdateEventForm(request.POST, request.FILES)
        if form.is_valid():
            event_obj = form.save(commit=False)
            event_obj.owner = request.user
            event_obj.save()
            return redirect('event-list')

    context = {
        'form':form,
    }
    return render(request, 'add_event_test.html', context)

def update_event(request, event_slug):
    event = Event.objects.get(slug=event_slug)
    # permission
    if not (request.user.is_authenticated and event.owner == request.user):
        return redirect('login')

    data = {
        'title':event.title,
        'description':event.description,
        'location':event.location,
        'datetime':event.datetime,
        'seats':event.seats,
        'reserved_seats':event.reserved_seats,
        }
    form = AddUpdateEventForm(instance=event)
    if request.method == "POST":
        form = AddUpdateEventForm(request.POST, request.FILES, instance=event, initial=data)
        if form.is_valid() and form.has_changed():
            form.save()
            return redirect('event-list')
    
    context = {
        'form':form,
        'event':event, 
    }
    return render(request, 'update_event_test.html', context)


def organizer_events(request, organizer_username):
    #used in my dashboard
    #permissions
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(username=organizer_username)
    events = user.event_set.all().order_by('-datetime')
    if request.GET.get('past'):
        events = user.event_set.filter(datetime__lte=datetime.today()).order_by('-datetime')
    if request.GET.get('all'):
        events = user.event_set.all().order_by('-datetime')
    if request.GET.get('upcoming'):
        events = user.event_set.filter(datetime__gt=datetime.today()).order_by('-datetime')

    context = {
        'events':events, 
        'is_following': user.followers.filter(follower=request.user).exists(),
        'user':user,
    }
    return render(request, 'organizer_list_test.html', context)

# View personal info in beautifull way
def personal_info(request, user_username):
    #permission
    if not request.user.is_authenticated or not user_username == request.user.username:
        return redirect('login')

    form = PersonalInfoUpdate(instance=request.user)
    context = {
        'form':form,
    }
    return render(request, 'update_personal_info.html', context)


def personal_info_update(request, user_username):
    #permission
    if not request.user.is_authenticated or not user_username == request.user.username:
        return redirect('login')

    data = {
        'username':request.user.username,
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'email':request.user.email,
        }
    form = PersonalInfoUpdate(instance=request.user)
    if request.method == "POST":
        form = PersonalInfoUpdate(request.POST, request.FILES, instance=request.user, initial=data)
        if form.is_valid() and form.has_changed():
            form.save()
            return redirect('event-list')
    
    context = {
        'form':form,
        'user_username':user_username,
    }
    return render(request, 'update_personal_info.html', context)

def change_pssword(request, user_username):
    #permission
    if not request.user.is_authenticated or not user_username == request.user.username:
        return redirect('login')

    form = ChangePasswordForm()
    if request.method == "POST":
        form = ChangePasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.set_password(user_obj.password)
            user_obj.save()
            login(request, user_obj)
            messages.success(request, "You have successfully changed password.")
            return redirect('event-list')
    
    context = {
        'form':form,
    }
    return render(request, 'update_password.html', context)

def follow(request, user_username):
    # permission user can't add itself
    if user_username == request.user.username or not request.user.is_authenticated:
        return redirect('event-list')

    following = User.objects.get(username=user_username)
    new_connection = Connection(following=following, follower=request.user)
    new_connection.save()
    return redirect('organizer-event-list', organizer_username=user_username)

def unfollow(request, user_username):
    # permission user can't add itself
    if user_username == request.user.username or not request.user.is_authenticated:
        return redirect('event-list')

    following = User.objects.get(username=user_username)
    Connection.objects.filter(following=following, follower=request.user).delete()
    return redirect('organizer-event-list', organizer_username=user_username)
    


