from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    class Meta:
        db_table='categories'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table='brands'

    def __str__(self):
        return self.name


import json

class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField(null=True,blank=True)
    id_category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    id_brand=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True)
    status_choices=(
        (0,'New'),
        (1,'Sale'))
    status=models.IntegerField(choices=status_choices,default=0)
    sale_percentage=models.IntegerField(null=True,blank=True)
    id_user=models.ForeignKey('users.CustomUser',on_delete=models.SET_NULL,null=True,blank=True)
    CompaniProFile=models.CharField(max_length=200,null=True,blank=True)
    images = models.JSONField(default=list)
    class Meta:
        db_table='products'

    def __str__(self):
        return self.name

    @property
    def get_image_list(self):
        if isinstance(self.images, str):
            try:
                valid_json_string = self.images.replace("'", '"')
                return json.loads(valid_json_string)
            except:
                return []
        return self.images if self.images else []

