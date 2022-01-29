from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.conf import settings

class UserMaster(AbstractUser):
    username = None
    first_name = None
    last_name = None
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    userType = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userType']

    objects = CustomUserManager()
    def __str__(self):
        return self.email

class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    birthDate = models.DateField(null=True)
    gender = models.CharField(max_length=6)
    bloodGroup = models.CharField(max_length=3)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10) 
    orderTime = models.DateTimeField(auto_now_add=True)
    pincode = models.IntegerField()
    vehicleModel = models.CharField(max_length=50)
    vehicleNumber = models.CharField(max_length=10)
    uid = models.ForeignKey(UserMaster ,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.firstName + " " + self.lastName

class Admin(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    contact =models.CharField(max_length=10)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ECC(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    contact =models.CharField(max_length=10)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    modelNumber = models.CharField(max_length=10, unique=True)
    allocationTime = models.DateTimeField(default= None)
    productTime = models.DateTimeField(auto_now_add=True,blank=True)
    cid = models.ForeignKey(Customer,on_delete=models.CASCADE,default= None)

    def __str__(self):
        return self.modelNumber

class PendingOrders(models.Model):
    oid = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

class AccidentRecords(models.Model):
    rid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Customer,on_delete=models.CASCADE)
    eid = models.ForeignKey(ECC,on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20) 
    longitude = models.CharField(max_length=20)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    area = models.CharField(max_length=80)
    pincode = models.CharField(max_length=8)
    time = models.DateTimeField(auto_now_add=True)
    replyTime = models.DateTimeField(auto_now_add=True)
    replyStatus = models.BooleanField()
    
    def __str__(self):
        return self.state

class Subscribers(models.Model):
    sid = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100,unique=True)
    time = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
         return self.Email