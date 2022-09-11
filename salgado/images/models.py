from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from datetime import datetime

from .convert_image import resize_and_convert

# Create your models here.

class Image(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='./uploaded_images')
    created_at = models.DateTimeField(auto_now_add=True)
    converted_image = models.ImageField(upload_to='./converted_images', editable=False)

    viewable = models.BooleanField(default=False)
    last_shown = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return mark_safe('<img src="/directory/%s" width="150" height="150" />' % (self.image))

    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        if not self.converted_image:
            self.converted_image = resize_and_convert(self.image)
        super().save(*args, **kwargs)
