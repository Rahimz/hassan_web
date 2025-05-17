from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from tools.models import TimeStampedModel, ActiveManager
from tools.make_thumbnail import make_thumbnail
from tools.hijri_to_gregory import hij_to_greg

class Gallery(TimeStampedModel):
    class ZoneChoices(models.TextChoices):
        GALLERY = 'gallery', _("Gallery")
        CERT = 'cert', _("Certificate")
    
    zone = models.CharField(
        max_length=12,
        choices=ZoneChoices.choices,
        default=ZoneChoices.GALLERY
    )  
    name = models.CharField(
        _("Name"),
        max_length=150,
    )
    description = models.TextField(
        blank=True
    )
    rank = models.PositiveSmallIntegerField(
        default=1
    )
    
    class Meta:
        ordering = ('rank',)
         
    def get_cover(self):
        return self.images.filter(cover_image=True).last()
    
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
    rank = models.PositiveSmallIntegerField(
        default=1
    )
    description = models.TextField(
        blank=True
    )
    back_description = models.TextField(
        blank=True
    )
    
    file = models.ImageField(
        _("File"),
        upload_to='images/'        
    )
    thumb = models.ImageField(
        _("Thumbnail"),
        upload_to='images/thumbs/',
        null=True,
        blank=True
    )
    image_alt = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    cover_image = models.BooleanField(
        default=False
    )
    file_local_path = models.CharField(
        max_length=350,
        null=True,
        blank=True
    )
    back_file = models.ImageField(
        _("Back File"),
        upload_to='images/',
        null=True,
        blank=True
    )    
    back_thumb = models.ImageField(
        _("Back Thumbnail"),
        upload_to='images/thumbs/',
        null=True,
        blank=True
    )
    back_image_alt = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    back_file_local_path = models.CharField(
        max_length=350,
        null=True,
        blank=True
    )
    
    date = models.DateField(
        blank=True,
        null=True
    )
    h_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    h_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    h_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    
    active = models.BooleanField(
        default=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )
    short_uuid = models.CharField(
        max_length=8,
        null=True,
        blank=True
    )
    
    objects = models.Manager()
    actives = ActiveManager()
    
    class Meta:
        ordering = ('rank',)
        
    def __str__(self):
        return self.title
    
    def get_type(self):
        return 'image'
    
    def get_absolute_url(self):
        return reverse("galleries:image_details", kwargs={"short_uuid": self.short_uuid})
    
    def get_hijri(self):
        return f"{self.h_year if self.h_year else '--'}/{self.h_month if self.h_month else '--'}/{self.h_day if self.h_day else '--'}"
    
    def save(self, *args, **kwargs):
        if not self.image_alt:
            self.image_alt = self.title
        if not self.back_image_alt:
            self.back_image_alt = self.title
            
        if not self.short_uuid:
            self.short_uuid = str(self.uuid)[:6]
        
        if self.h_year and not self.date:
            # print('date conversion starts')
            # if h_year exists we produce a date 
            year = self.h_year
            month = self.h_month if self.h_month else 1
            day = self.h_day if self.h_day else 1
            try:
                date = hij_to_greg(year, month, day) 
                # print('date convert')
            except:
                date = 'error'
            
            if date != "error":
                self.date = date
                # print('date saved')
            
        try:
            if self.file and not self.thumb:
                self.thumb = make_thumbnail(self.file.file, size=(500,500))
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
        
        try:
            if self.back_file and not self.back_thumb:
                self.back_thumb = make_thumbnail(self.back_file.file, size=(500,500))
        except Exception as e:
            print(f"Error generating thumbnail: {e}")

        return super().save(*args, **kwargs)