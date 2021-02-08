from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class gbagUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name

class userList(models.Model):
    user = models.ForeignKey(gbagUser, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Item(models.Model):
    STATUS = (
        ('BOUGHT', 'BOUGHT'),
        ('NOT AVAILABLE', 'NOT AVAILABLE'),
        ('PENDING', 'PENDING'),
    )
    userlist = models.ForeignKey(userList, on_delete=models.SET_NULL, blank=True, null=True)
    item_name = models.CharField(max_length=200, null=True)
    item_quantity = models.CharField(max_length=200, null=True)
    item_status = models.CharField(max_length=200, null=True, choices=STATUS)
    date = models.DateField(null=True)

    def __str__(self):
        return self.item_name