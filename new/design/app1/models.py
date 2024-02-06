from django.db import models

# Create your models here.
class Place(models.Model):
    name=models.CharField(max_length=50)
    desc=models.CharField(max_length=500)
    image=models.ImageField(upload_to="app1/image",null=True,blank=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name=models.CharField(max_length=50)
    desc=models.TextField()
    image=models.ImageField(upload_to="team/image",null=True,blank=True)

    def __str__(self):
        return self.name