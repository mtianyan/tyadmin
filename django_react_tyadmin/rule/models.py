from django.db import models


# Create your models here.
class Rule(models.Model):
    key = models.IntegerField()
    disabled = models.BooleanField
    href = models.CharField(max_length=36)
    avatar = models.CharField(max_length=134)
    name = models.CharField(max_length=24)
    owner = models.CharField(max_length=6)
    desc = models.CharField(max_length=12)
    call_no = models.IntegerField()
    status = models.CharField(max_length=2)
    updated_at = models.CharField(max_length=48)
    created_at = models.CharField(max_length=48)
    progress = models.IntegerField()


class Meta:
    verbose_name = 'Rule'
    verbose_name_plural = verbose_name


def __str__(self):
    return self.name
