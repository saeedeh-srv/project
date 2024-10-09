from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile




class UserRegisterForm(forms.ModelForm):
    password_1 = forms.CharField(max_length=100, required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'id': 'form3Example5',
                                         'type': 'password',
                                     }
                                 ))
    username = forms.CharField(required=True, max_length=50,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'id': 'form3Example1'
                                   }
                               ))
    email = forms.EmailField(required=True, max_length=175,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'id': 'form3Example2'
                                 }
                             ))
    first_name = forms.CharField(required=True, max_length=50,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'id': 'form3Example3'
                                     }
                                 ))
    last_name = forms.CharField(required=True, max_length=50,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'id': 'form3Example4'
                                    }
                                ))
    phone_number = forms.CharField(required=True, max_length=12,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'id': 'form3Example7',
                                           'name': 'phone_number'
                                       }
                                   ))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('this user name was taken')
        return username

    def clean_password_1(self):
        password1 = self.cleaned_data['password_1']
        if len(password1) < 8:
            raise forms.ValidationError('something went wrong')
        return password1

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Profile.objects.filter(phone=phone_number).exists():
            raise forms.ValidationError('this phone already exists')
        return phone_number


class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'form3Example4'}))
    remember = forms.BooleanField(required=False,
                                  widget=forms.CheckboxInput(
                                      attrs={
                                          'class': 'form-check-input me-2',
                                          'id': 'form2Example33'
                                      }
                                  ))
    username = forms.CharField(
        required=True, max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'form3Example1'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'username or password is incorrect'
        super().__init__(*args, **kwargs)


class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['phone', 'image']

    def __init__(self, *args, **kwargs):
        # Pop the user instance from the kwargs and pass it to both forms
        user = kwargs.pop('user', None)
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

        # If a user is passed, prepopulate User fields
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super(UserProfileUpdateForm, self).save(commit=False)

        # Save the User model fields
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile
