from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "password",
            "confirm_password",
        ]

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return confirm_password

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        print("# UserRegistrationForm.save() user: ", user)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
