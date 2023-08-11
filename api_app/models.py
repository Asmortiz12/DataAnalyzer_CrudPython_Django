from django.db import models

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    names = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100, default='true')
    carrer = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)

    def __str__(self):
        return self.names
