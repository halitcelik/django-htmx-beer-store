from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.


class AdminGroup(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)
    name = models.CharField(max_length=223)


class AdminGroupItem(models.Model):
    group = models.ForeignKey(AdminGroup, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey("content_type", "object_id")
