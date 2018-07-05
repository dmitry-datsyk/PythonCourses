from string import Template

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ImageField
from django.utils.safestring import mark_safe

from ProjectMy.models import Shop, Item


class SimpleForm(forms.Form):
    title = forms.CharField(
        label='Название', max_length=20)
    price = forms.IntegerField(label='Цена', min_value=5, max_value=3000)
    is_sold = forms.BooleanField(label='Продано')
    creation_date = forms.DateField(
        label='Дата создания', widget=forms.TextInput(attrs={'class': 'datepicker'}))


# class ItemCreateForm(forms.Form):
#     name = forms.CharField(
#         label='Название товара', max_length=20)
#     description = forms.CharField(label='Описание', widget=forms.Textarea)
#     price = forms.IntegerField(label='Цена', min_value=5, max_value=3000)
#     is_sold = forms.BooleanField(label='Продано')
#     creation_date = forms.DateField(
#         label='Дата создания', widget=forms.TextInput(attrs={'class': 'datepicker'}))


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))


class ItemCreateForm(forms.ModelForm):
    class Meta:
        image = ImageField(widget=PictureWidget)
        model = Item
        fields = ('name', 'description','price', 'is_sold','department',
                'creation_date', 'image')



class SearchForm(forms.Form):
    min_price = forms.IntegerField(label='Минимальная цена', min_value=0,
                                   max_value=10**12, required=False)
    max_price = forms.IntegerField(label='Максимальная цена', min_value=0,
                                   max_value=10**12, required=False)
    part_name = forms.CharField(label='Часть названия', max_length=10, required=False)
    is_sold = forms.BooleanField(label='Продано', required=False)
    shop = forms.ModelChoiceField(label='Магазин',
            queryset= Shop.objects.all(), required=False )

    def clean_part_name(self):
        if ' ' in self.cleaned_data['part_name']:
            raise ValidationError('Ведите слово без пробелов')
        return self.cleaned_data['part_name']