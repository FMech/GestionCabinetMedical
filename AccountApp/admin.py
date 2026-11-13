from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Doctor, Patient, Specialty

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Specialty)