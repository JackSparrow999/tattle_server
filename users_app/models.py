from django.db import models

# Create your models here.
class User(models.Model):

    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def verify_password(self, pw):

        return pw == self.password

#article
# many to many relationship
class Room(models.Model):

    name = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    users = models.ManyToManyField(User)