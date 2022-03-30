from django.db import models


# Create your models here.

class UserSubscription(models.Model):
    rule = models.CharField(max_length=255, unique=True)
    subscription = models.CharField(max_length=555)

    def __str__(self):
        return self.rule
