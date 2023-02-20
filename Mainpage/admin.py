from django.contrib import admin
from .models import Myfiles
# Register your models here.

admin.site.register(Myfiles)
class FileAdmin(admin.ModelAdmin):
    list_display = ["file_id","my_file"]