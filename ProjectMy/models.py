from django.db import models


class Shop(models.Model):

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Адрес')
    staff_amount = models.IntegerField(verbose_name='Количество сотрудников')


class Department(models.Model):


    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'

    def __str__(self):
        return '{}. {}'.format(self.id, self.sphere)

    sphere = models.CharField(max_length=100, verbose_name='Область')
    staff_amount = models.IntegerField(verbose_name='Количество сотрудников')
    description = models.TextField(verbose_name='Описание отделов',  )
    shop = models.ForeignKey(
        Shop, related_name='departments', on_delete=models.CASCADE, verbose_name='ID магазина')



class Item(models.Model):


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return '[{} | Item {} from {}]'.format(self.id, self.name, self.department.shop.name)

    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена')
    department = models.ForeignKey(
        Department, related_name='items', on_delete=models.CASCADE, verbose_name='ID области')
    image = models.ImageField(upload_to='items/', verbose_name='Изображение',
                              null=True, blank=True)
    is_sold = models.BooleanField(verbose_name='Продан', default=False)
    creation_date = models.DateField(verbose_name='Дата создания', null=True, blank=True)
# Create your models here.
