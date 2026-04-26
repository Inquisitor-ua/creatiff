from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=64, verbose_name='Тест')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'