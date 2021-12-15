
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from hotel_app.models import *

from django.forms import ModelForm


## Login Form gamit niya yung login_view 
class LoginForm(forms.Form):
    #username = forms.CharField(max_length=63)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


## Registration From for account 
class RegistrationGuestForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Guest
        fields = ['first_name','last_name', 'email','phone', 'password1', 'password2',]


##BookingView form_class 
class BookingForm(ModelForm):
   # checkin_date = forms.CharField(widget=forms.widgets.DateTimeInput())
    class Meta:
        model = Booking
        fields = ["hotel_code","room_ID","checkin_date","checkout_date","no_of_guests"]
        

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['room_ID'].queryset =  Room.objects.filter(is_available=True)
        #self.fields['guest_name'].queryset =  

        
## Contact form 

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"

class ReviewForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['comment']

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['card_owner','card_number','card_cvv','exp_month','exp_year']

