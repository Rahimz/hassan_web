from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

from tools.models import TimeStampedModel, ActiveManager
from tools.make_thumbnail import make_thumbnail


class Gallery(TimeStampedModel):
    name = models.CharField(
        _("Name"),
        max_length=150,
    )
    
    def __str__(self):
        return self.name


class Image(TimeStampedModel):
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.SET_NULL,
        related_name='images',
        null=True,
        blank=True
    )
    title = models.CharField(
        _("Title"),
        max_length=150,
    )
    file = models.ImageField(
        _("File"),
        upload_to='images/'        
    )
    thumb = models.ImageField(
        _("Thumbnail"),
        upload_to='images/thumbs/'
    )
    image_alt = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    active = models.BooleanField(
        default=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )
    
    objects = models.Manager()
    actives = ActiveManager()
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        try:
            if not self.thumb:
                self.thumb = make_thumbnail(self.file.file, size=(500,500))
        except:
            pass

        return super().save(*args, **kwargs)