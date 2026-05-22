from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=64, verbose_name='Test')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

class ContactModel(models.Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=16, verbose_name="Phone number")
    message = models.TextField(verbose_name="Message text")
    datetime = models.DateTimeField(verbose_name="Date and time of the request", auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Contact form"
        verbose_name_plural = "Contact forms"

