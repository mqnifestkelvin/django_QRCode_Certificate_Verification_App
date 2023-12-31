# Generated by Django 4.2.5 on 2023-10-14 14:05

import certificate.utils
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='certificate.faculty')),
            ],
            options={
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('student_image', models.ImageField(upload_to=certificate.utils.student_image_upload_path)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('course_name', models.CharField(max_length=100)),
                ('student_cgpa', models.FloatField()),
                ('student_status', models.CharField(choices=[('Awaiting graduation', 'Awaiting Graduation'), ('Graduated', 'Graduated')], max_length=100)),
                ('issue_date', models.DateField()),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('encrypted_byte_code', models.CharField(blank=True, max_length=255)),
                ('encrypted_byte_code_redirect_link', models.CharField(blank=True, max_length=255)),
                ('qr_code_image', models.ImageField(blank=True, editable=False, upload_to='QRcodes/')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='certificate.department')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='certificate.faculty')),
            ],
            options={
                'verbose_name_plural': 'Certificates',
            },
        ),
    ]
