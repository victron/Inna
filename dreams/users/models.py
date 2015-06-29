from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from django.utils import timezone


# Create your models here.

# class MyUser(User):
#     # email = models.EmailField(
#     #     verbose_name='email address',
#     #     max_length=255,
#     #     unique=True,
#     # )
#     email = User.email
#     class Meta:
#         proxy = True

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



# class User_mod(User):
#
#
#     class Meta:
#         proxy = True
#         User._meta.get_field('email').unique = True

