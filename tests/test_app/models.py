from django.db import models


class TestModel(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    birth = models.DateField()
    phone = models.IntegerField()