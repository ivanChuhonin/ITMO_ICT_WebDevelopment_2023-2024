from django import  forms
from .models import Guest, Review
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):

    class Meta:
        model = Guest
        # Add fields we will be collecting info for
        fields = ['first_name', 'last_name', 'username', 'password']

    # DO form cleaning here
    def clean_username(self):
        username = self.cleaned_data['username']
        if Guest.objects.filter(username=username).exists():
            raise ValidationError('Username is not available')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # check password length
        if len(password) < 8:
            raise ValidationError("Password can't be less than 8 characters")
        # check for number and letters is password
        if password.isalpha() or password.isnumeric():
            raise ValidationError("Password should contains both letters and numbers")

        return password


class AgreementForm(forms.Form):
    date_from = forms.DateField()
    date_to = forms.DateField()


class ReviewForm(forms.Form):
    room = forms.CharField(required=False, disabled=True)
    date_from = forms.DateField(required=False, disabled=True)
    date_to = forms.DateField(required=False, disabled=True)
    comment = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField()
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    date_review = forms.DateField(required=False, disabled=True)
