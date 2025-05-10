from io import BytesIO
from django.core.files import File
from PIL import Image as IMG
from PIL import ImageDraw, ImageFont
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
            
            # resize image            
            im.thumbnail(size) # resize image

            # Add watermark +++++
            watermark_text = "agharebparast.ir"
            
            # Create a drawing context
            draw = ImageDraw.Draw(im)
            
            # Calculate a reasonable font size based on image dimensions
            width, height = im.size
            font_size = int(min(width, height) * 0.05)  # 5% of the smaller dimension
            
            try:
                # Try to load a font (you might need to provide a font file)
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback to default font if specific font not available
                font = ImageFont.load_default()
            
            # Get text bounding box using textbbox
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]  # right - left
            text_height = text_bbox[3] - text_bbox[1]  # bottom - top
            
            # Calculate text position (bottom right corner with some padding)
            margin = 10
            x = width - text_width - margin
            y = height - text_height - margin
            
            # Add semi-transparent text
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
            # Add watermark +++++
            
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
    
