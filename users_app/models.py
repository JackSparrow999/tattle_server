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
    super_users = (User)
    users = models.ManyToManyField(User)


class SuperRelation(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    room = models.OneToOneField(Room, on_delete=models.DO_NOTHING)