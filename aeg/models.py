from django.db import models

# Create your models here.


class Topics(models.Model):
    topic_name = models.CharField(max_length=100)

    def __str__(self):
        return self.topic_name

class Essays(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='Essays/uploaded/')
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, default="1")
    evaluated = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Report(models.Model):
    essay = models.ForeignKey(Essays, on_delete=models.CASCADE)
    report = models.FileField(upload_to='Essays/Report/')

    # def __str__(self):
    #     return self.report

class Bow(models.Model):
    BEST = 'B'
    AVERAGE = 'A'
    COMMON = 'C'
    PRIORITY_OF_WORD = [
        (BEST, 'Best'),
        (AVERAGE, 'Average'),
        (COMMON, 'Common'),
    ]
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_OF_WORD,
        default=BEST,
    )
