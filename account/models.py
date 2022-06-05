from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .send_email import send_notification


class Usermanager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('the given email must be set')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, password, email, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('superboy must have status "is_staff"=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('superboy must have status "is_superuser"=True')
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    second_name = models.CharField(max_length=100, blank=True)
    objects = Usermanager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(_('active'), default=False, help_text='Designates whether this user should be treated as active.''Unselect this instead of deleting account')
    is_author = models.BooleanField(_('author'), default=False, help_text='Designates whether this user should be treated as author.''Unselect this instead of deleting account')

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code


from django.contrib.auth import get_user_model
User = get_user_model()


class Follower(models.Model):
    singer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed', null=True)
    listener = models.ForeignKey(User,on_delete=models.CASCADE, related_name='followers')


@receiver(post_save, sender=Follower)
def order_post_save(sender, instance, *args, **kwargs):
    send_notification(instance.listener, instance.singer)
