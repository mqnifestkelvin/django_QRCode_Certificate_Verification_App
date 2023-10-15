from django.db import models
from django.urls import reverse
import hashlib
import time
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import student_image_upload_path, generate_qr_code
from django.utils.text import slugify
import uuid


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list-faculty', args=[self.slug])
    

class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, related_name='department', on_delete=models.CASCADE, null=True) 
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list-department', args=[self.slug])


class Certificate(models.Model):
    student_image = models.ImageField(upload_to=student_image_upload_path)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, related_name='certificates', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='department', on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=100)
    student_cgpa = models.FloatField()
    student_status = models.CharField(max_length=100, choices=[('Awaiting graduation', 'Awaiting Graduation'), ('Graduated', 'Graduated'),])
    issue_date = models.DateField()
    slug = models.SlugField(max_length=100,blank=True)
    encrypted_byte_code = models.CharField(max_length=255, blank=True, editable=True)
    encrypted_byte_code_redirect_link =  models.CharField(max_length=255, blank=True, editable=True)
    qr_code_image = models.ImageField(upload_to='QRcodes/', blank=True, editable=False)

    class Meta:
        verbose_name_plural = 'Certificates'

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('certificate-info', args=[self.slug])


# Hashing Logic
def generate_encrypted_byte_code(instance):
    data = f"{instance.last_name}{str(time.time())}"
    encoded = hashlib.sha256(data.encode()).hexdigest()[:30]
    return f"http://127.0.0.1:8000/existqr/{encoded}"


# Signal Logic
@receiver(pre_save, sender=Certificate)
def save_encrypted_byte_code(sender, instance, **kwargs):
    if not instance.encrypted_byte_code:
        instance.encrypted_byte_code = generate_encrypted_byte_code(instance)[30:]

    if not instance.encrypted_byte_code_redirect_link:
        instance.encrypted_byte_code_redirect_link = generate_encrypted_byte_code(instance)
         
         # QR Code logic
        qr_code_filename = f"{instance.first_name}_{instance.last_name}_QRcode.png"
        qr_code_path = os.path.join('QRcodes', qr_code_filename)
        generate_qr_code(instance.encrypted_byte_code_redirect_link, qr_code_path)


@receiver(pre_save, sender=Certificate)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.encrypted_byte_code)


@receiver(pre_save, sender=Certificate)
def reset_values_on_save(sender, instance, **kwargs):
    if Certificate.objects.filter(pk=instance.id).exists():
        original_instance = Certificate.objects.get(pk=instance.id)

        # Resetting the fields to their original values
        instance.slug = original_instance.slug
        instance.encrypted_byte_code = original_instance.encrypted_byte_code
        instance.encrypted_byte_code_redirect_link = original_instance.encrypted_byte_code_redirect_link
        instance.qr_code_image = original_instance.qr_code_image


