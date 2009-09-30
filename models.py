from django.contrib.auth.models import User
from django.db import models
    
class FacebookUser(models.Model):
        facebook_id = models.CharField(max_length=100, unique=True)
        contrib_user = models.OneToOneField(User)
        contrib_password = models.CharField(max_length=100)

