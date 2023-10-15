import os
from django.conf import settings
import qrcode

def student_image_upload_path(instance, filename):
    """
    Generate path for saving student images.
    """
    # extract file extension
    ext = filename.split('.')[-1]
    
    # renaming the file using the student's name and adding the extension
    filename = f"{instance.first_name}_{instance.last_name}.{ext}"

    # return the upload path
    return os.path.join('student_images', filename)


def generate_qr_code(data, path):
    """
    Generate a QR code for given data and save it to the provided path.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Ensure the path directories exist
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    directory = os.path.dirname(full_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    img.save(full_path)
