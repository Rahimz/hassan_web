from django.db import models
from tools.gregory_to_hijri import hij_strf_date, greg_to_hij_date


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True, status='publish')
     
class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    class Meta: 
        abstract = True 
    
    
    def get_fa_created(self):
        return hij_strf_date(greg_to_hij_date(self.created.date()), '%-d %B %Y')
    
    def get_fa_updated(self):
        return hij_strf_date(greg_to_hij_date(self.updated.date()), '%-d %B %Y')
    
    def get_fa_end_access(self):
        if self.end_access:
            return hij_strf_date(greg_to_hij_date(self.end_access.date()), '%-d %B %Y')

    def get_fa_start_access(self):
        if self.start_access:
            return hij_strf_date(greg_to_hij_date(self.start_access.date()), '%-d %B %Y')
    
    def get_fa_date(self):
        if self.date:
            return hij_strf_date(greg_to_hij_date(self.date.date()), '%-d %B %Y')
    
    def get_fa_start(self):
        if self.start_time:
            return hij_strf_date(greg_to_hij_date(self.start_time.date()), '%-d %B %Y')
    
    def get_fa_end(self):
        if self.end_time:
            return hij_strf_date(greg_to_hij_date(self.end_time.date()), '%-d %B %Y')
        
    def get_fa_completed(self):
        if self.completed_date:
            return hij_strf_date(greg_to_hij_date(self.completed_date.date()), '%-d %B %Y')
    
    def get_fa_opened(self):
        if self.opened_at:
            return hij_strf_date(greg_to_hij_date(self.opened_at.date()), '%-d %B %Y')
    
    def get_fa_user_viewed(self):
        if self.user_date_viewed:
            return hij_strf_date(greg_to_hij_date(self.user_date_viewed.date()), '%-d %B %Y')
    
    def get_fa_start_register(self):
        if self.start_register:
            return hij_strf_date(greg_to_hij_date(self.start_register.date()), '%-d %B %Y')
    
    def get_fa_end_register(self):
        if self.end_register:
            return hij_strf_date(greg_to_hij_date(self.end_register.date()), '%-d %B %Y')
        

    def save(self, *args, **kwargs):
        """
        Overriding the save method in order to make sure that
        modified field is updated even if it is not given as
        a parameter to the update field argument.
        """
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'updated'})

        super().save(*args, **kwargs)