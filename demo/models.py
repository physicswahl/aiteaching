from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    math_performance = models.FloatField(help_text="Score from 0 to 10")
    reading_writing_performance = models.FloatField(help_text="Score from 0 to 10")
    eligible_for_support = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

