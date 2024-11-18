from django.db import models

from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_mb = 5  # Set max file size in MB
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size cannot exceed {max_size_mb} MB.")

def validate_file_extension(file):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']  # Allowed extensions
    import os
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in allowed_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}. Allowed extensions: {', '.join(allowed_extensions)}.")

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/', validators=[validate_file_size, validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
