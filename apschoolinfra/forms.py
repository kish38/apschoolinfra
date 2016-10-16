from django import forms
from .models import *

class TeacherForm(forms.Form):
    school_code = forms.CharField()
    username = forms.EmailField(label="E-mail")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password (again)")

    def clean_school_code(self):
    	if not School.objects.filter(pk=self.cleaned_data["school_code"]):
    		raise forms.ValidationError("Invalid School Id")
    	return self.cleaned_data["school_code"]

    def clean_username(self):            
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.")
        else:
            return self.cleaned_data['username']

    def clean(self):            
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data

class DeviceForm(forms.ModelForm):
	class Meta:
		model = Device
		fields = ('device_name','status')

class IncidentForm(forms.ModelForm):
	class Meta:
		model = Incident
		fields = ('creater','device','title','description','status')

class LoginForm(forms.Form):
	username = forms.CharField(label="username")
	password = forms.CharField(widget=forms.PasswordInput, label="Password")