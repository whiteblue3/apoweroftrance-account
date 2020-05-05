from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from .models import User
from .access_log import *
from .util import accesslog


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `User` instance is created. If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)


@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    accesslog(
        request, ACCESS_TYPE_AUTHENTICATE, ACCESS_STATUS_SUCCESSFUL,
        user.email, request.META['REMOTE_ADDR']
    )


@receiver(user_logged_out)
def sig_user_logged_out(sender, user, request, **kwargs):
    accesslog(
        request, ACCESS_TYPE_LOGOUT, ACCESS_STATUS_SUCCESSFUL,
        user.email, request.META['REMOTE_ADDR']
    )
