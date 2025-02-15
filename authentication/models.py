from django.db import models
from mandate.models import Office
from django.contrib.auth.models import User

class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    office = models.ForeignKey(Office, on_delete=models.PROTECT)