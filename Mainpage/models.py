from django.db import models

# Create your models here.
class Myfiles(models.Model):
    file_id = models.AutoField
    my_file = models.FileField(upload_to="mydoc")
    