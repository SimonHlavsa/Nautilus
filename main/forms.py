from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)