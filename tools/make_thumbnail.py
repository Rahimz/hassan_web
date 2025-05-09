from io import BytesIO
from django.core.files import File
from PIL import Image as IMG
import os


def make_thumbnail(image, size=(500, 500)):
    """Makes thumbnails of given size from given image"""
    thumbnail = None
    # im = IMG.open(image)
    try:
        with IMG.open(image) as im:
            if im.mode in ('RGBA', 'P'):
                im = im.convert('RGB') # convert mode

            # extension = image.name.split('.')[-1]
            image_name, image_ext = os.path.splitext(os.path.basename(image.name))

            im.thumbnail(size) # resize image

            thumb_io = BytesIO() # create a BytesIO object
            # we have problem with gif image so if the save method doesnot work we do not 
            # make any thumbnail
             # Save the thumbnail based on format
            if image_ext.lower() in ('.jpg', '.jpeg'):
                format = 'JPEG'
            elif image_ext.lower() == '.png':
                format = 'PNG'
            elif image_ext.lower() == '.webp':
                format = 'WEBP'
            else:
                # Default to JPEG for other formats
                format = 'JPEG'
                image_ext = '.jpg'
                    
            try:
                im.save(thumb_io, format, quality=85) #, quality=85 save image to BytesIO object
            except Exception as e:
                print(f"Error creating thumbnail: {e}")
                return thumbnail
            # image_name = image.name.split('/')[-1]
            thumbnail = File(thumb_io, name=f"{image_name}{image_ext}") # create a django friendly File object
    except Exception as e:
        print(f"Error creating thumbnail main: {e}")   
    return thumbnail
    
