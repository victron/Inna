from django.db import models

# Create your models here.
class User(models.Model):
    login = models.CharField(max_length = 255)
    email = models.EmailField()
    registration_date = models.DateTimeField('Registration Date')

    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)

    def __unicode__(self):
        return unicode({'login' : self.login,
                'email' : self.email,
                'registration_date' : self.registration_date,
                'firstName' : self.firstName,
                'lastName' : self.lastName,
                })



class Dreams(models.Model):
    dream_subject = models.CharField('subject of dream', max_length = 255)
    dream_text = models.TextField('dream description')
    dream_date = models.DateField('morning date')
    user = models.ForeignKey(User)

    def __str__(self):
        return unicode({'dream_subject' : self.dream_subject,
                'dream_text' : self.dream_text,
                'dream_date' : self.dream_date,
                'user' : self.user,
                })

