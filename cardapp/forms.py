from dal import autocomplete
from django import forms
from colorfield.widgets import ColorWidget
from django.core import validators
from .models import *

class BackgroundForm(forms.ModelForm):
    class Meta:
        model = Background
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput,
            'color_bg': ColorWidget,
        }

    def __init__(self, *args, **kwargs):  # no user here
        user = kwargs.pop('user', None)
        super(BackgroundForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(username=user)

class CreateBlockForm(forms.ModelForm):
    class Meta:
        model = CreateBlock
        fields = '__all__'
        widgets = {'user': forms.HiddenInput}

    def __init__(self, *args, **kwargs):  # no user here
        user = kwargs.pop('user', None)
        super(CreateBlockForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(username=user)



class CreateFaqForm(forms.ModelForm):
    class Meta:
        model = CreateFaq
        fields = '__all__'
        widgets = {'block': forms.HiddenInput,
                   'user': forms.HiddenInput}

    def __init__(self, *args, **kwargs):  # no user here
        user = kwargs.pop('user', None)
        super(CreateFaqForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(username=user)
        self.fields['block'].queryset = CreateBlock.objects.filter(user=user)

class TableCategoryForm(forms.ModelForm):
    class Meta:
        model = TableCategory
        fields = '__all__'
        widgets = {'block': forms.HiddenInput,
                   'user': forms.HiddenInput}

    def __init__(self, *args, **kwargs):  # no user here
        user = kwargs.pop('user', None)
        super(TableCategoryForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(username=user)
        self.fields['block'].queryset = CreateBlock.objects.filter(user=user)


class TableItemsForm(forms.ModelForm):
    class Meta:
        model = TableItems
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput,
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                  forward=['block']
                                                  )
        }

class AddImageForm(forms.ModelForm):
    class Meta:
        model = AddImage
        fields = '__all__'
        widgets = {'block': forms.HiddenInput,
                   'user': forms.HiddenInput}

    def __init__(self, *args, **kwargs):  # no user here
        user = kwargs.pop('user', None)
        super(AddImageForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(username=user)
        self.fields['block'].queryset = CreateBlock.objects.filter(user=user)

class AddVideoForm(forms.ModelForm):
    class Meta:
        model = YoutubeVideo
        fields = '__all__'
        widgets = {'block': forms.HiddenInput,
                   'user': forms.HiddenInput}

    def __init__(self, *args, **kwargs):  # no user here
        user = kwargs.pop('user', None)
        super(AddVideoForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(username=user)
        self.fields['block'].queryset = CreateBlock.objects.filter(user=user)

class CreateLinkForm(forms.ModelForm):
    class Meta:
        model = CreateLink
        fields = '__all__'
        widgets = {
            'status': forms.Select,
            'user': forms.HiddenInput,
            'block': forms.HiddenInput,
            'color_icon': ColorWidget,
            'color_bg': ColorWidget,
            'choose': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):  # no user here
        user = kwargs.pop('user', None)
        super(CreateLinkForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(username=user)
        self.fields['block'].queryset = CreateBlock.objects.filter(user=user)

class CardProfileForm(forms.ModelForm):
    class Meta:
        model = CardProfile
        fields = '__all__'