from django.contrib import admin
from django import forms

from .models import Image, Gallery
from tools.utils.read_local_file import ReadLocalFile

class ImageAdminForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        file_local_path = cleaned_data.get('file_local_path')
        
        # If no file was uploaded but local path is provided
        if not file and file_local_path:
            try:
                # Open the local file and create a File object
                cleaned_data['file'] = ReadLocalFile(file_local_path)
                    
            except IOError:
                raise forms.ValidationError("Could not read file from the provided local path")
        
        # Ensure we have either a file or a local path
        if not file and not file_local_path:
            raise forms.ValidationError("Either a file must be uploaded or a local file path must be provided")
        
        return cleaned_data
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    list_display = ['id', 'title', 'gallery', 'rank', 'active', 'short_uuid', 'file_size_mb']
    list_filter = ['gallery']
    search_fields = ['id', 'uuid', 'short_uuid', 'title', 'description']
    list_editable =['rank']
    def file_size_mb(self, obj):
        if obj.file:
            size_bytes = obj.file.size
            size_mb = size_bytes / (1024 * 1024)  # Convert bytes to MB
            return f"{size_mb:.2f} MB"  # Format to 2 decimal places
        return "0 MB"
    file_size_mb.short_description = 'File Size (MB)'  # Sets column header
    
    # Optional: Make file not required in admin since we're handling it in the form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['file'].required = False
        return form

     # Optional: If you want to show file_local_path more prominently
    fieldsets = (
        (None, {
            'fields': ('title', 'gallery', 'rank', 'description', 'back_description')
        }),
        ('Files', {
            'fields': ('file', 'file_local_path', 'back_file', 'back_file_local_path'),
            'description': 'Either upload a file or provide a local path'
        }),
        ('Thumbnails', {
            'fields': ('thumb', 'back_thumb'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('date', 'h_year', 'h_month', 'h_day', 'active', 'short_uuid'),
            'classes': ('collapse',)
        }),
        ('Alt Texts', {
            'fields': ('image_alt', 'back_image_alt'),
            'classes': ('collapse',)
        }),
    )
    
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rank', 'zone']
    list_editable = ['rank']