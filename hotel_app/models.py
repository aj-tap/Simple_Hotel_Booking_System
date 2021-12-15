from django.db import models

# Create your models here.
from datetime import datetime,date,timedelta

## lib for models auto creation in Invoice 
from django.dispatch import receiver
from django.db.models.signals import post_save

## Custom accounts model 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Guest(AbstractUser):
    date_of_birth = models.DateField(null=True)
    phone = models.CharField(max_length=12, help_text="+63", null=True,)
    email = models.EmailField(('email address'), unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


    def __str__(self):
        return str(self.email)
    
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not full_name:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.full_name = full_name
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = is_active
        user.save(using=self._db)
        return user

    
    class Meta:
        verbose_name = 'Guest List'
          


class Hotel(models.Model):
    hotel_code = models.BigAutoField(primary_key=True,unique=True)   # PK 
    name = models.CharField(max_length=200)
    location= models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    hotel_email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPES = [
           ('Studio', 'Studio room'),
    ('standard', 'Standard room'),
    ('family', 'Family room'),
        ]
    room_no=models.IntegerField(default=101)
    hotel_code=models.ForeignKey(Hotel,null=True,on_delete=models.CASCADE)
    
    room_type=models.CharField(max_length=200,default='standard', choices=ROOM_TYPES)
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_available=models.BooleanField(default=True)
    no_of_beds=models.IntegerField(default=3)
    description = models.CharField(max_length=100, null=True)
    room_img = models.ImageField(upload_to='images', null=True)
    
    def __str__(self):
        return str( "Room " + str(self.room_no) + "-"+ self.room_type)

    def hotel_name(self):
        return self.hotel.name

    class Meta:
        verbose_name = 'Hotel Room'
          

class Booking(models.Model):
    booking_num = models.BigAutoField(primary_key=True, unique=True)
    guest_ID=models.ForeignKey(Guest,on_delete=models.CASCADE)
    hotel_code=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    room_ID=models.ForeignKey(Room,on_delete=models.CASCADE,null=True)  

    checkin_date=models.DateTimeField(default=datetime.now())
    checkout_date=models.DateTimeField(default=datetime.now() + timedelta(days=1))
    check_out=models.BooleanField(default=False)
    
    no_of_guests=models.IntegerField(default=1)

    def compute_charges(self):
        time_delta = self.checkout_date - self.checkin_date
        total_time = time_delta.days
        total_cost =total_time*self.room_ID.rate
        # return total_cost
        return total_cost

    def charge(self):
      if self.check_out:
          if self.checkin_date==self.checkout_date:
              return self.room_ID.rate
          else:
              time_delta = self.checkout_date - self.checkin_date
              total_time = time_delta.days
              total_cost =total_time*self.room_ID.rate
              return total_cost
      else:
          return 'Calculated when checked out'
    
    def number_of_days(self):
        time_delta = self.checkout_date - self.checkin_date
        return time_delta.days


    def __str__(self):
       if self.guest_ID == None:
           return str(self.booking_num)
       else:
           return str( "BK-"+ str(self.booking_num) + "_" + str(self.hotel_code) + "_" + self.guest_ID.email )


    class Meta:
        verbose_name = 'Booking List'
          
    
class Rating(models.Model):
    guest_ID=models.ForeignKey(Guest,on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=12)
    

##Payment 

class Payment(models.Model):
    booking_num = models.ForeignKey(Booking, on_delete=models.CASCADE)
    card_owner = models.CharField(null=True, max_length=32)
    card_number = models.IntegerField(null=True,max_length=16)
    card_cvv = models.IntegerField(null=True, max_length=3,)
    exp_month = models.IntegerField(null=True,max_length=2)
    exp_year = models.IntegerField(null=True,max_length=4)


@receiver(post_save,sender=Booking)
def  RType(sender, instance, created, **kwargs):
    room = instance.room_ID
    if created:
        room.is_available = False
    room.save()
    if instance.check_out ==True:
        room.is_available=True
    room.save()    