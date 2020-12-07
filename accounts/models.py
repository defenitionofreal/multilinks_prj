from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import MyUsernameValidator # для валидации по символам

from django.dispatch import Signal
from .utilities import send_activation_notification

from django.urls import reverse
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True,
        validators=[MyUsernameValidator()],
        error_messages={
            'unique': ("Этот логин занят. Попробуйте другой."),
        },
    )
    phone = models.CharField(max_length=12, blank=True)
    age = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to='images/users/', blank=True)
    title = models.CharField(max_length=35, blank=True)
    description = models.CharField(max_length=81, blank=True)
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активизацию?')

    #def get_absolute_url(self):
    #    return reverse('create_links', kwargs={"slug": self.username})

# письмо для активации
user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispatcher)