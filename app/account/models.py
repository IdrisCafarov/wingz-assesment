from django.db import models

# Create your models here.



from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self,email,password=None,is_active=True, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)



class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True,max_length=120, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    name = models.CharField(max_length=40,verbose_name="Name", blank=True, null=True)
    surname = models.CharField(max_length=40,verbose_name="Surname", blank=True, null=True)


    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('driver', 'Driver'),
        ('rider', 'Rider'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='rider')

    timestamp = models.DateTimeField(auto_now_add=True)


    
    is_active = models.BooleanField(default=True)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'MyUser'
        verbose_name_plural = 'MyUser'


    def __str__(self):
        return f"{self.email}"


    def get_full_name(self):
        if self.surname:
            return '%s %s'%(self.name,self.surname)
        return self.name

    def has_perm(self,perm,obj=None):
        return self.role == 'admin'

    def has_module_perms(self, app_label):
        if self.role in ['admin', 'staff']:
            return True  
        return False
    
    @property
    def is_staff(self):
        """Return True if the user is admin or staff."""
        return self.role in ['admin', 'staff']




