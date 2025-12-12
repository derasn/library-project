from django.db import models
from django.core.exceptions import ValidationError
import os


def validate_file_extension(value):
    extension = os.path.splitext(value.name)[1].lower()

    valid_extensions = ['.pdf', '.docx', '.pptx', '.jpeg', '.png']

    if extension not in valid_extensions:
        raise ValidationError("This file type is not supported. Try uploading a PDF, DOCX, PPTX, JPEG or PNG.")
        

def validate_file_size(value):
    file_size = value.size

    max_size = 10 * 1024 * 1024

    if file_size > max_size:
        raise ValidationError("The file you're trying to upload is too large. Maximum size allowed is 10MB.")


# Create your models here.

class Subject(models.Model):
    name = models.CharField(null=False)

    def __str__(self):
        return f"{self.name}"
    
    @property
    def has_materials(self):
        return Material.objects.filter(course_code__subject=self).exists()
    


class Course(models.Model):
    course_code = models.CharField(max_length=16)
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    level = models.CharField(null=True)
    featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.course_code} - {self.title}"
    
    


class Material(models.Model):
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials")
    description = models.TextField(blank=False, default="Past questions")
    year_used = models.IntegerField(null=False)
    file = models.FileField(upload_to='materials/', validators=[validate_file_extension, validate_file_size] , null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    no_of_downloads =  models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.course_code} - {self.description}"