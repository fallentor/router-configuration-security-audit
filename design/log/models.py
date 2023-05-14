from django.db import models

# Create your models here.


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    request_method = models.CharField(max_length=10)
    request_url = models.CharField(max_length=200)
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    is_logged_in_first_time = models.BooleanField(null=True,default=False)

