from django.db import models
from django.contrib.auth.models import User

class Script(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='scripts/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title