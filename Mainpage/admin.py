from django.contrib import admin
from .models import Myfiles,ContactForm
# Register your models here.

admin.site.register(Myfiles)
admin.site.register(ContactForm)
class FileAdmin(admin.ModelAdmin):
    list_display = ["file_id","my_file"]