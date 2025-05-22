from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):

    ADMIN = 'Admin','Admin'

    STUDENT = 'Student','Student'

    INSTRUCTOR = 'Instructor','Instructor'


class Profile(AbstractUser):

    # image = models.ImageField(upload_to='profile-images/')

    role = models.CharField(max_length=15,choices=RoleChoices.choices)

    def __str__(self):

        return f'{self.first_name}-{self.last_name}-{self.role}'
    
    class Meta:

        verbose_name = 'Profile'

        verbose_name_plural = 'Profile'