from django.db import models

import uuid


# Create your models here.

category_choices =[
    ('IT & Softwares','IT & Softwares'),
    ('Finance','Finance'),
    ('Marketing','Marketing')
]
  

class BaseClass(models.Model):

    uuid = models.SlugField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True
    

class CategoryChoices(models.TextChoices):


    # variable = 'value','representation'

    IT_SOFTWARES = 'IT & Softwares','IT & Softwares'

    FINANCE = 'Finance','Finance'

    MARKETING = 'Marketing','Marketing'


class LevelChoices(models.TextChoices):

    BEGINNER = 'Beginner','Beginner'

    INTERMEDIATE = 'Intermediate','Intermediate'

    ADVANCED = 'Advanced','Advanced'

class TypeChoices(models.TextChoices):

    FREE = 'Free','Free'

    PREMIUM = 'Premium','Premium'


class Courses(BaseClass):

    '''
    title
    description
    image
    instructor
    category
    level
    fee
    offer_fee
    
    '''

    title = models.CharField(max_length=50)

    description = models.TextField()

    image = models.ImageField(upload_to='course-images/')
                                   #app name.modelname

    instructor = models.ForeignKey('instructors.Instructors',on_delete=models.CASCADE)

    # category = models.CharField(max_length=25,choices=category_choices) defining choices as list of tuple method
    category = models.CharField(max_length=25,choices=CategoryChoices.choices)  # defining choices as class by inherit textChoices class

    level = models.CharField(max_length=25,choices=LevelChoices.choices)

    type = models.CharField(max_length=15,choices=TypeChoices.choices)

    tags = models.TextField()

    fee = models.DecimalField(max_digits=8,decimal_places=2)

    offer_fee = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)


    # 120.00

    def __str__(self):

        return f'{self.title}-{self.instructor}'
    


    class Meta :

        verbose_name = 'Courses'

        verbose_name_plural = 'Courses'

        ordering =['id']
    