from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=64, verbose_name='Тест')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

class ContactModel(models.Model):
    name = models.CharField(max_length=128, verbose_name="Ім'я")
    email = models.EmailField(verbose_name="Електронна пошта")
    phone = models.CharField(max_length=16, verbose_name="Номер телефону")
    message = models.TextField(verbose_name="Текст повідомлення")
    datetime = models.DateTimeField(verbose_name="Дата та час звернення", auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone} - {self.message}"

    class Meta:
        verbose_name = "Контактна форма"
        verbose_name_plural = "Контактні форми"