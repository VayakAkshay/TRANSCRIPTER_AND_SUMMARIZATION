from django.db import models

# Create your models here.
class Myfiles(models.Model):
    file_id = models.AutoField
    my_file = models.FileField(upload_to="mydoc")
    

class ContactForm(models.Model):
    email = models.EmailField(max_length=200,default=0)
    message = models.TextField(max_length=5000,default="")

    def __str__(self):
        return self.email