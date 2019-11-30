from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=50, blank=True, default="Anon")
    face_encoding = models.CharField(max_length=9999)


class Photo(models.Model):
    image = models.ImageField(upload_to='')
    persons = models.ManyToManyField(
        to=Person, related_name='persons_in_image')
