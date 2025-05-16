from django.contrib import admin

from .models import Image, Gallery


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'gallery', 'rank', 'active', 'short_uuid', 'file_size_mb']
    
    def file_size_mb(self, obj):
        if obj.file:
            size_bytes = obj.file.size
            size_mb = size_bytes / (1024 * 1024)  # Convert bytes to MB
            return f"{size_mb:.2f} MB"  # Format to 2 decimal places
        return "0 MB"
    file_size_mb.short_description = 'File Size (MB)'  # Sets column header

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rank', 'zone']
    list_editable = ['rank']