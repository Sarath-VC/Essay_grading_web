from django.db import models

# Create your models here.
class Essays(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='Essays/uploaded/')

    def __str__(self):
        return self.title