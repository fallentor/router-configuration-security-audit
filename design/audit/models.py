from django.db import models

# Create your models here.


class AuditResult(models.Model):
    id = models.AutoField(primary_key=True)
    sort_id = models.IntegerField(null=False)
    address = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=50, default='无', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name or self.address
