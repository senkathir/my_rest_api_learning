from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings#used to retreive setting(AUTH_USER_MODEL) from our django proj(profiles_project)
# Create your models here.

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None):#passwd can be none also
        """Create new user profile"""
        if not email:
            raise ValueError('User must have an email id')
        email = self.normalize_email(email)#normalize the frst half of email i.e. case sensitive and second half will be case insensitive
        user = self.model(email=email,name=name)#creates new model for this manager with the input args
        user.set_password(password)#uses AbstractBaseUser for password hashing (using set_password)
        user.save(using=self._db)#save to db

        return user

    def create_superuser(self, email, name, password):
        """Create superuser"""
        user = self.create_user(email, name, password)

        user.is_superuser = True#from PermissionsMixin
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """DB model for users"""
    email = models.EmailField(max_length=255, unique=True)#creates a "email" column in userprofile table
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()#for managing this model which overrides the default user model   #Custom manager for overriding default
    USERNAME_FIELD = 'email'#instead of default login with username, use email in place of username
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retreive full name of user"""
        return self.name

    def get_short_name(self):
        """Retreive short name of user"""
        return self.name
    def __str__(self):
        """String reprensentation of model"""
        return self.email#we ll usually specify the field with which we will identify the model

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as string"""
        return self.status_text#when model is converted to string, status will be returned
