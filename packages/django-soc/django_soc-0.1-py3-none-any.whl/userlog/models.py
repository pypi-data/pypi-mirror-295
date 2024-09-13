from django.db import models


class UserLog(models.Model):
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=255,blank=False,null=True)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.ip_address} visited {self.path} at {self.timestamp}"
