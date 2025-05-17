from django.core.files.base import ContentFile
import re, os
from django.conf import settings

    
def ReadLocalFile(file_path, main_folder='sources', file_name=None):
    
    """
    Get the local file path and return it as a django file instance to save in models.FileField.
    
    Args:
        file_path: Path to the file relative to the sources/ folder (e.g., "sources/2/we_34_3.jpg")
        main_folder: Base folder (default: 'sources') where files are stored
        file_name: Optional new name for the file (without extension)
    
    Returns:
        django.core.files.base.ContentFile instance
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the path points to a directory
    """
    # Prevent directory traversal and absolute paths
    if os.path.isabs(file_path):
        raise ValueError("Absolute paths are not allowed")
    
    # Construct full path safely
    full_path = os.path.join(main_folder, file_path)
    full_path = os.path.normpath(full_path)  # Clean up path (e.g., remove ../)
    
    # Security check: Ensure the path remains under main_folder
    if not os.path.realpath(full_path).startswith(os.path.realpath(main_folder)):
        raise ValueError("Invalid file path - directory traversal detected")
    
    # Make path absolute if it isn't already
    if not os.path.isabs(file_path):
        file_path = os.path.join(settings.BASE_DIR, file_path)
    
    # Check file existence
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")
    if not os.path.isfile(full_path):
        raise ValueError(f"Path is not a file: {full_path}")
    
    
    # Open and read the file
    with open(full_path, 'rb') as f:
        file_content = f.read()
    
    # Handle filename
    if file_name:
        # Keep original extension if new name is provided
        _, ext = os.path.splitext(file_path)
        new_file_name = f"{file_name}{ext}"
    else:
        # Use original filename
        new_file_name = os.path.basename(file_path)
    
    # Create Django file
    django_file = ContentFile(file_content)
    django_file.name = new_file_name
    
    return django_file
    
# def RemoveImageExtraPath(path):
#     """
#     remove 'https://atmancenter.org/wp-content/' from the begining of thumbnail url
#     """
#     pattern = r'uploads/.*$'
#     match = re.search(pattern, path)
#     return match.group(0)

# def make_django_file(path, filename):
#     # new_path = RemoveImageExtraPath(path)
#     django_image_file = ReadLocalFile(path, filename)
#     return django_image_file