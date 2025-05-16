from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid 

from tools.models import TimeStampedModel, ActiveManager
from tools.hijri_to_gregory import hij_to_greg


class Entry(TimeStampedModel):
    title = models.CharField(
        max_length=150
    )
    description = models.TextField(
        blank=True
    )
    date = models.DateField(
        blank=True,
        null=True
    )
    h_year = models.PositiveSmallIntegerField(
        default=1320
    )
    h_month = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    h_day = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    
    link  = models.URLField(
        blank=True,
        null=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )
    
    active = models.BooleanField(
        default=True
    )
    
    
    objects = models.Manager()
    actives = ActiveManager()
    
    class Meta:
        ordering = ('date', 'id')
    
    def get_type(self):
        return 'entry'
    
    def Hijri(self):
        return f"{self.h_year}, {self.h_month}, {self.h_day}"
    def save(self, *args, **kwargs):
        if hij_to_greg(self.h_year, self.h_month, self.h_day) != "error" and not self.date:
            self.date = hij_to_greg(self.h_year, self.h_month, self.h_day)
        
        return super().save(*args, **kwargs)
