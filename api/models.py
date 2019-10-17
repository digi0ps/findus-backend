from django.db import models

# Create your models here.


class FaceEncoding(models.Model):
    person_name = models.CharField(max_length=50, blank=True, default="Anon")
    encoding = models.CharField(max_length=9999)


class Photo(models.Model):
    image = models.ImageField(upload_to='')
    persons = models.ManyToManyField(
        to=FaceEncoding, null=True)
