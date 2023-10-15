from django.contrib import admin
from . models import Certificate, Department, Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('encrypted_byte_code',)}