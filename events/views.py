from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventBookingForm, AddUpdateEventForm
from .models import Event, Booking
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
    # permission (only organizer)
    # in HTML 

    context = {
        'event': event,
    }
    return render(request, 'detail_test.html', context)
 
# ----- All Registered user -----

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
    form = AddUpdateEventForm(initial=data)
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
