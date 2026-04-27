from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class TrackingLink(models.Model):
    code = models.SlugField(unique=True)
    source_name = models.CharField(max_length=100)
    target_url = models.URLField()
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code