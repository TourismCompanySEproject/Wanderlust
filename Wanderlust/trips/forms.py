from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreditCardField(forms.IntegerField):
    def get_cc_type(self,number):
        number = str(number)


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length = 30, required = True, widget= forms.EmailInput())
    #credit_card_no = CreditCardField(forms.Form, required=True, label= "Credit Card")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')