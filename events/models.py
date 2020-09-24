from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from django.template.defaultfilters import slugify 


class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    location = models.TextField()
    datetime = models.DateTimeField()
    seats = models.IntegerField()
    reserved_seats = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    #image = models.ImageField()

    def __str__(self):
        return self.title


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    creation_date = models.DateTimeField(auto_now_add=True)
    seats = models.IntegerField()

    def __str__(self):
        return self.event.title


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()


class Connection(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Event.objects.filter(slug=slug)
    if qs.exists():
        try:
            int(slug[-1])
            if "-" in slug:
                slug_list = slug.split("-")
                new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
            else:
                new_slug = "%s-1" % (slug)
        except:
            new_slug = "%s-1" % (slug)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Event)
def auto_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

# Update reserved seats when add, update or cancel booking
@receiver(post_save, sender=Booking)
def update_reserved_seats_on_update_create(instance, created, *args, **kwargs):
    event = instance.event 
    event.reserved_seats = event.reserved_seats + instance.seats
    event.save()

@receiver(pre_delete, sender=Booking)
def update_reserved_seats_on_delete(instance, *args, **kwargs):
    event = instance.event
    event.reserved_seats = event.reserved_seats - instance.seats
    event.save()





# Follow 

    