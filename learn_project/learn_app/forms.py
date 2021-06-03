from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    # title = forms.CharField(max_length=150, label='Название',
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # content = forms.CharField(label='Текст', required=False,
    #                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    # is_published = forms.BooleanField(label='Опубликовано?', initial=True,
    #                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    # category = forms.ModelChoiceField(empty_label='Выберите категорию',
    #                                   queryset=Category.objects.all(), label='Категория',
    #                                   widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = News
        # fields = '__all__' - все поля сразу (но так лучше не делать)
        fields = ['title', 'content', 'is_published', 'category']
        # список полей для формы
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        # виджеты и html классы к ним

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title