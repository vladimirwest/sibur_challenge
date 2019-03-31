from django.db import models

class Users(models.Model):
    login = models.CharField(max_length=10)
    passw = models.CharField(max_length=200)
    role = models.CharField(max_length=1)

class ReactorOne(models.Model):
    grate0_1 = models.FloatField()
    grate0_2 = models.FloatField()
    grate0_3 = models.FloatField()
    grate0_4 = models.FloatField()
    grate1_1 = models.FloatField()
    grate1_2 = models.FloatField()
    grate11_1 = models.FloatField()
    grate11_2 = models.FloatField()
    grate11_3 = models.FloatField()
    grate11_4 = models.FloatField()
    grate12_1 = models.FloatField()
    grate12_2 = models.FloatField()
    grate4_1 = models.FloatField()
    grate4_2 = models.FloatField()
    grate4_3 = models.FloatField()
    grate4_4 = models.FloatField()
    grate8_1 = models.FloatField()
    grate8_2 = models.FloatField()
    grate8_3 = models.FloatField()
    grate8_4 = models.FloatField()
    timestamp = models.DateTimeField(blank=True)