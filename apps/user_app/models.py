from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

from ..admin_app import models as admin_app_models

# Create your models here.

class UserManager(BaseUserManager):

    def generate_user_id(self):
        last_object = self.model.objects.all().order_by('id').last()
        if last_object and last_object.id.startswith("user"):
            try:
                new_user_count = int(last_object.id.split("user")[-1]) + 1
            except ValueError:
                new_user_count = 1
        else:
            new_user_count = 1
        return "user{:06d}".format(new_user_count)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(id=self.generate_user_id(), email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    

class User(AbstractBaseUser):
    
    id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username=models.CharField(max_length=50, null=True, blank=True)
    full_name=models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    country_code = models.CharField(max_length=10, default="+91")
    phone = models.CharField(max_length=20, null=True, unique=True)
    password = models.CharField(max_length=255, null=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = User.objects.generate_user_id()

        if not self.username:
            self.username = self.email

        if not self.full_name:
            self.full_name = self.first_name + " " + self.last_name
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} - {self.last_name} - {self.email}"

    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def is_user_staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def is_user_superuser(self):
        "Is the user a admin member?"
        return self.is_superuser


class Task(models.Model):
    app = models.ForeignKey(admin_app_models.App, related_name='tasks', on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
    user = models.ForeignKey('user_app.User', related_name='tasks', on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Task for {self.app.name} by {self.user.full_name}'