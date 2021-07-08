from django.db import models
import hashlib

# Create your models here.
class User(models.Model):

    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def verify_password(self, pw):

        return pw == self.password


# many to many relationship
class Room(models.Model):

    name = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    admins = models.ManyToManyField(User)
    users = models.ManyToManyField(User)

    def verify_access_token(self, token):

        return token == self.access_token