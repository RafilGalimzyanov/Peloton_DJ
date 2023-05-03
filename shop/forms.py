from django import forms
from django.core.exceptions import ValidationError

from shop.models import *



class SearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Поиск'}
        )
    )


class OrderModelForm(forms.ModelForm):
    DELIVERY_CHOICES = (
        (0, 'Выберите, пожалуйста'),
        (1, 'Доставка'),
        (2, 'Самовывоз'),
    )
    DELIVERY_TIME_CHOICES = (
        (0, 'Время доставки'),
        (1, '8:00-10:00'),
        (2, '11:00-13:00'),
        (3, '14:00-16:00'),
        (4, '17:00-20:00'),
    )
    delivery = forms.TypedChoiceField(label='Доставка', choices=DELIVERY_CHOICES, coerce=int)
    time_delivery = forms.TypedChoiceField(label='Время доставки', choices=DELIVERY_TIME_CHOICES, coerce=int)

    class Meta:
        model = Order
        exclude = ['discount', 'status', 'need_delivery', 'date_delivery']
        labels = {'address': 'Полный адрес (Улица, дом, квартира)'}
        widgets = {
            'address': forms.Textarea(
                attrs={'rows': 6, 'cols': 80, 'placeholder': 'При самовывозе можно оставить это поле пустым'}
            ),
            'notice': forms.Textarea(
                attrs={'rows': 6, 'cols': 80}
            )
        }

    def clean_delivery(self):
        data = self.cleaned_data['delivery']
        if data == 0:
            raise ValidationError('Необходимо выбрать способ доставки')
        return data

    def clean_time_delivery(self):
        data = self.cleaned_data['time_delivery']
        if data == 0:
            raise ValidationError('Необходимо выбрать время доставки')
        return data

    def clean(self):
        try:
            delivery = self.cleaned_data['delivery']
            address = self.cleaned_data['address']
            if delivery == 1 and address == '':
                raise ValidationError('Укажите адрес доставки')
            return self.cleaned_data
        except KeyError:
            pass


class ReviewForm(forms.Form):
    email = forms.EmailField(label="Почта")
    name = forms.CharField(max_length=100, label="Имя")
    rev = forms.CharField(widget=forms.Textarea(attrs={"cols": 60, "rows": 7}),
                          label="Отзыв")