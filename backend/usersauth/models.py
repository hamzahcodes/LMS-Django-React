from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    This model overrides the default Django user model to use `email` as the 
    unique identifier for authentication instead of `username`. It includes 
    additional fields such as `full_name` and `otp`.

    Fields:
        username (str): A unique username used for display or reference.
        email (str): A unique email address used as the primary identifier for login.
        full_name (str): Full name of the user, auto-filled from email if empty.
        otp (str): One-time password or token used for verification/authentication.

    Notes:
        - `USERNAME_FIELD` is set to `email`, meaning users log in with their email.
        - `REQUIRED_FIELDS` only includes `username` since `email` is required by default.
        - If `full_name` or `username` is not provided, it is auto-derived from the email's local part (before '@').

    Methods:
        __str__(): Returns the user's email as string representation.
        save(): Auto-populates `username` and `full_name` before saving, if not provided.
    """
    
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(unique=True, max_length=100)
    otp = models.CharField(unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        email_username, full_name = self.email.split('@')

        if self.full_name == '' or self.full_name == None:
            self.full_name = email_username

        if self.username in ['', None]:
            self.username = email_username

        super(User, self).save(*args, **kwargs)
    

class Profile(models.Model):
    """
    Custom Profile model extending Django's Model.

    This model overrides the default Django user model to use `email` as the 
    unique identifier for authentication instead of `username`. It includes 
    additional fields such as `full_name` and `otp`.

    Fields:
        username (str): A unique username used for display or reference.
        email (str): A unique email address used as the primary identifier for login.
        full_name (str): Full name of the user, auto-filled from email if empty.
        otp (str): One-time password or token used for verification/authentication.

    Notes:
        - `USERNAME_FIELD` is set to `email`, meaning users log in with their email.
        - `REQUIRED_FIELDS` only includes `username` since `email` is required by default.
        - If `full_name` or `username` is not provided, it is auto-derived from the email's local part (before '@').

    Methods:
        __str__(): Returns the user's email as string representation.
        save(): Auto-populates `username` and `full_name` before saving, if not provided.
    """
    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_folder', default='default-user.jpg', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)
        
    def save(self, *args, **kwargs):
        if self.full_name in ['', None]:
            self.full_name = self.user.full_name
        super(Profile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)