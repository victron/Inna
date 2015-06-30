from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from django.utils import timezone


# Create your models here.

class Dreams(models.Model):
    dream_subject = models.CharField('subject of dream', max_length = 255)
    dream_text = models.TextField('dream description')
    dream_date = models.DateTimeField('morning date',  auto_now_add=True, auto_now=False )
    user = models.ForeignKey(User)

    def __str__(self):
        return unicode({'dream_subject' : self.dream_subject,
                'dream_text' : self.dream_text,
                'dream_date' : self.dream_date,
                'user' : self.user,
                })


class D_Tags(models.Model):
    d_tag = models.CharField('Dream tag', max_length=255)
    d_description = models.TextField('Dream tag description')


class Dreams_D_Tags(models.Model):
    WEIGHT_CHOISES = ((1, '1'), (2, '2'), (3, '3'), (4, '4') , (5, '5'))
    dream_tag_weight = models.IntegerField(choices=WEIGHT_CHOISES, default=5)
    dream_tag_id = models.ManyToManyField(D_Tags)
    dream_id = models.ManyToManyField(Dreams)

# ---------------- Event model ----------------------

class Event(models.Model):
    # WEIGHT_CHOISES = (1, 2, 3, 4, 5)
    WEIGHT_CHOISES = ((1, '1'), (2, '2'), (3, '3'), (4, '4') , (5, '5'))
    event_weight = models.IntegerField(choices=WEIGHT_CHOISES, default=5)
    event_subject = models.CharField('Event subject', max_length=255)
    event_text = models.TextField('Event text')
    event_date = models.DateTimeField('Event date and time')
    user = models.ForeignKey(User)


# class E_Tags(models.Model):
#     tag = models.CharField('Event tag')
#     description = models.TextField('Event tag description')

class Event_D(models.Model):
    # WEIGHT_CHOISES = (1, 2, 3, 4, 5)
    # E_D_weight = models.CharField(max_length=1, choices=WEIGHT_CHOISES, default=5)
    event_id = models.ManyToManyField(Event)
    dream_id = models.ManyToManyField(Dreams)
    # event_tag_id = models.ManyToManyField(E_Tags)



