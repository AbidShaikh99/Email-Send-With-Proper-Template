from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.email
