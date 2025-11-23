from django import forms
from .models import User, UserLanguage, Language

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'bio', 'birth_date', 'native_language', 'timezone', 'goals', 'interests']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'goals': forms.CheckboxSelectMultiple(),
            'interests': forms.CheckboxSelectMultiple(),
        }

class UserLanguageForm(forms.ModelForm):
    class Meta:
        model = UserLanguage
        fields = ['language', 'proficiency']
