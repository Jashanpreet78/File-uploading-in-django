from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)
    title = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='files/pdfs/')
    

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)