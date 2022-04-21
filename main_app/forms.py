from django import forms
from .models import Profile

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['location', 'avatar']
        # widgets = {
        #     'birthdate': DateInput(attrs={'type': 'date'}),
        # }