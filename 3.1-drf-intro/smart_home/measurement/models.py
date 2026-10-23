from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='measurements',
        verbose_name='Датчик',
    )
    temperature = models.FloatField(verbose_name='Температура')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время измерения')

    image = models.ImageField(
        upload_to='measurements/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )