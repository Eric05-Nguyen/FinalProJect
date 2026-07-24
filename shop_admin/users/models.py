from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name=models.CharField(max_length=100)
    class Meta:
        db_table='countries'

    def __str__(self):
        return self.name    
class CustomUser(AbstractUser):
    avatar=models.ImageField(upload_to='avatar/',null=True,blank=True)
    id_country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    

    class Meta:
        db_table='custom_user'


