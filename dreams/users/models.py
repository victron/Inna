from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Dreams(models.Model):
    dream_subject = models.CharField('subject of dream', max_length = 255)
    dream_text = models.TextField('dream description')
    dream_date = models.DateTimeField('morning date', default=timezone.now )
    user = models.ForeignKey(User)

    def __str__(self):
        return unicode({'dream_subject' : self.dream_subject,
                'dream_text' : self.dream_text,
                'dream_date' : self.dream_date,
                'user' : self.user,
                })
