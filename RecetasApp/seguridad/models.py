from django.db import models
from django.contrib.auth.models import User


class UsersMetadata(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    token = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_users} {self.last_name}"
    
    class Meta:
        verbose_name = 'User metadata'
        verbose_name_plural = 'Users metadata'