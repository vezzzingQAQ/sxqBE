from django.db import models
from django.forms import CharField

# Create your models here.


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=5)
    cid = models.CharField(max_length=20)
    c_class = models.CharField(max_length=15)
    c_class_id = models.IntegerField(default=0)
    voice = models.IntegerField(default=0)
    record = models.IntegerField(default=0)
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(str(self.id) + " " + self.name + " " + self.c_class + " " + str(self.c_class_id) + " " + str(self.voice) + " " + str(self.record) + " " + str(self.visit_time))
