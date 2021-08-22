from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class UserForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=200)
    last_name = forms.CharField(required=False, max_length=200)
    groups = forms.ModelMultipleChoiceField(required=True,queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "groups")
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
        return user