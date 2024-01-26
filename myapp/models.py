from django.db import models
from django.contrib.auth.models import User

class mapPointers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rate = models.IntegerField()
    photo = models.ImageField()

    def __str__(self):
        return f'MapPointer {self.id} - User: {self.user.username}'
