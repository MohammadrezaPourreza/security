from django.db import models
# Create your models here.

class attempts(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    host = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=150)
    content_type = models.CharField(max_length=50)
    content_length = models.IntegerField()
    country = models.CharField(max_length=100)
    att_date = models.DateTimeField('date of attempt')
    def __str__(self):
        return self.username
