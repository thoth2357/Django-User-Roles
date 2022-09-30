from enum import unique
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# For Fun i have changed the default login system to email login system instead f, email


##############MANAGERS#############################
class UserManager(BaseUserManager): #override the default user manager
    '''
    args:BaseUserManager
    purpose:OVerride the default user manager
    '''
    def _create_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):
        if not email:
            raise ValueError('Users must have an username')
        now = timezone.now()
        
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, is_active=True, **extra_fields):
        '''
        purpose: create a normal user by overriding the default create_user
        '''
        return self._create_user(email, password, False, False, is_active, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        '''
        purpose:create a superuser by overriding the default create_superuser
        '''
        user = self._create_user(email, password, True, True, True, **extra_fields)
        user.save(using=self._db)
        return user
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT # settting every user initially as student except specifially proven to be principal..Security kind of thing in my head
        return super().save(*args, **kwargs)

class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.TEACHER)

class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STUDENT)    

######################## MANAGERS END ###############################

############################ USER MODEL #################################3
class User(AbstractBaseUser, PermissionsMixin):
    'Abstract base user for all users'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Types(models.TextChoices):
        'Class to handle different user types'
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"
        PRINCIPAL = "PRINCIPAL", "PRINCIPAL"
    
    type = models.CharField(('Type'), max_length=50, choices=Types.choices, null=True)
    
    email = models.EmailField("Enter Email for login", max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    ######################## Decided to make use of Proxy models, as i find it more efficient and easier to use..ANd lol i hate long queries in my views ############################
    #And user types are automatically saved for me kinda.


########################### PROXY USER MODEL #####################################
class Teacher(User): 
    base_type = User.Types.TEACHER #this automatically saves the type for the Teacher Type of User
    objects = TeacherManager()

    @property
    def more(self): # this is a property that returns the teacher details attached to this user..The whole essence of using proxy models.Separate details from user.Attach them somewhere
        return self.teacherdetails
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.TEACHER
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True  #setting proxy to true

    def __str__(self):
        return f'{self.email}- {self.type}'


class Student(User):
    base_type = User.Types.STUDENT
    objects = StudentManager()

    @property
    def more(self): # this is a property that returns the teacher details attached to this user..The whole essence of using proxy models.Separate details from user.Attach them somewhere
        return self.studentdetails
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
        return super().save(*args, **kwargs)
    
    class Meta:
        proxy = True
    
    def __str__(self):
        return f'{self.email}-{self.type}'

class Principal(User):
    base_type = User.Types.PRINCIPAL

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.PRINCIPAL
        return super().save(*args, **kwargs)

####################################### USER DETAILS FOR PROXY #################################
class StudentDetails(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='upload/', null=True)
    Name = models.CharField(max_length=50,  help_text='Full Name', null=True)

    def __str__(self):
        return f'{self.user} {self.id}'
    
class TeacherDetails(models.Model):
    user = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50,  help_text='Full Name', null=True)
    title = models.CharField(max_length=50, null=True, default=None)
    Students = models.ManyToManyField(Student, blank=True, null=True, related_name="%(class)s_students")
    Bio = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return f"{self.user}-{self.Name}"




