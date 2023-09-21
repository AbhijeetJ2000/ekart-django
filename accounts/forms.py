from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'password': 'Enter Password',
            'confirm_password': 'Confirm Password',
        }

        for field_name, placeholder_text in placeholders.items():
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs['placeholder'] = placeholder_text
                field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )
        

