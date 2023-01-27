from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


# class ImageForm(forms.Form):
#     image = forms.ImageField(
#         widget=forms.FileInput(
#             attrs={"id": "image_field", style="height: 100px ; width : 100px ; "}
#     )

class SignInUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs=
                                                                         {'class': 'form-input',
                                                                          'type': 'password'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.TextInput(attrs=
                                                                                {'class': 'form-input',
                                                                                 'type': 'password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs=
                                                                        {'class': 'form-input',
                                                                         'type': 'password'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class PrivateNoteFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PrivateNoteFormMixin, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(user=self.request.user.id)
        self.fields['folder'].empty_label = "None"

    class Meta:
        model = Note
        exclude = ['user', 'slug']
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea'}),
            'folder': forms.Select(attrs={'class': 'form-select'})
        }


class AddFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        exclude = ['user', 'slug']
        fields = '__all__'
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'})}
