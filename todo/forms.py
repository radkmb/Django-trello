from django import forms
from django.contrib.auth.models import User

from .models import List, Card


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "email",)

class ListForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = List
        fields = ("title",)

class CardForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Card
        fields = ("title", "description", "list", "order")
        labels = {'title':'タイトル', 'description':'内容', 'list':'リスト', 'order':'優先度',}

class CardCreateFromHomeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CardCreateFromHomeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Card
        fields = ("title", "description", "order")
        labels = {'title':'タイトル', 'description':'内容', 'order':'優先度',}

class CardUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CardUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Card
        fields = ("title", "description", "list", "order")
        labels = {'title':'タイトル', 'description':'内容', 'list':'リスト', 'order':'優先度',}