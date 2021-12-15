from django.shortcuts import render, redirect, reverse
##
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
##
## models import 
from hotel_app.models import Booking, Room

## para naman sa Login, Register forms 
from hotel_app.forms import LoginForm, RegistrationGuestForm, BookingForm, ContactForm, PaymentForm
from django.contrib.auth.decorators import login_required ## for funciton views 
from django.contrib.auth.mixins import LoginRequiredMixin ## for class views

## related sa accounts 
from django.contrib.auth import login, authenticate, logout
## related sa contact email 
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

## google login
import requests
from datetime import datetime
#from urllib import urlencode
from django.conf import settings
from django.contrib import messages
#from app.models import User
from hotel_app.models import Guest as User 

#reviews NLP
from hotel_app.forms import ReviewForm
import pickle
import nltk

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, 'home.html', {})


class BookingView(LoginRequiredMixin,CreateView):
    model = Booking
    template_name = "booking.html"
    #success_url = '/receipt/'
    success_url = '/payment/'
    #fields = ["hotel_code","room_ID","checkin_date","checkout_date","no_of_guests"]
    form_class = BookingForm
    
    #def get_user(self):
    #    return self.request.user

    def form_valid(self, form):
        form.instance.guest_ID = self.request.user
        #bill = Bill(booking_num=form.instance.)
        #send email method 
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        content = super(BookingView, self).get_context_data(**kwargs)
        content['rooms'] = Room.objects.filter(is_available=True)
        
        return content 

    #def get_success_url(self, **kwargs):
    #    #return render(request, 'receipt.html', {Booking.objects.filter(guest_ID=self.request.user)})
#   #     context = {}
    #    context['booking_details'] = Booking.objects.get(booking_num=1)
#
    #    return render(self.request, 'receipt.html', context)
        

    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == 'room_ID':
    #        return CategoryChoiceField(queryset=Category.objects.all())
    #    return super().formfield_for_foreignkey(db_field, request, **kwargs)


# return redirect(reverse('story_detail', kwargs={'story':story.id}))

class BookingListView(LoginRequiredMixin,ListView):
    model = Booking
    template_name = "bookinglist.html"
    
    def get_context_data(self, **kwargs):
        content = super(BookingListView, self).get_context_data(**kwargs)
        #content['object'] = self.model.objects.all()
        #content['object'] = self.model.objects.get(guest_ID=self.request.user)
        #content['object'] = self.model.objects.filter(booking_num=12)
        #content['object'] = self.model.objects.filter(guest_ID='sample@b.com')
        content['object'] = self.model.objects.filter(guest_ID=self.request.user)
        return content 

@login_required
def receipt_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    content = {}
    last_booking_obj = Booking.objects.filter(guest_ID=request.user).last()
   
    return render(request, 'receipt.html', {'object':last_booking_obj})



def login_view(request):
    form = LoginForm()
    message = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.email} You have been Logged in'
                return redirect('home')
            else:
                message = 'Login Failed'
    return render(request,'login.html', context={'form':form, 'message': message})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    if request.method == "POST":
        form = RegistrationGuestForm(request.POST)
        if form.is_valid():
            #username=form.cleaned_data['username']
            #first_name=form.cleaned_data['first_name']
            #last_name=form.cleaned_data['last_name']
            #phone = form.cleaned_data['phone']
            #email = form.cleaned_data['email']
            #password1 = form.cleaned_data['paswword1']
            #password2 = form.cleaned_data['paswword2']
            form.save()
            #papunta sa login page, dapat may msg extra na account is created
            return redirect('login')
    else:
        form = RegistrationGuestForm()
    return render(request,'register.html',{'form':form})
    
def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            content = form.cleaned_data['content']
            try:
                send_mail(contact_name, contact_email, content, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('home') ## change to contact mesg
    return render(request, "contact.html", {'form': form})



## google login 
def google_login(request):
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse('google_login')
    )
    if('code' in request.GET):
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        url = 'https://accounts.google.com/o/oauth2/token'
        response = requests.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        response = requests.get(url, params={'access_token': access_token})
        user_data = response.json()
        email = user_data.get('email')
        if email:
            #user, _ = User.objects.get_or_create(email=email, username=email)
            user, _ = User.objects.get_or_create(email=email)
            gender = user_data.get('gender', '').lower()
            if gender == 'male':
                gender = 'M'
            elif gender == 'female':
                gender = 'F'
            else:
                gender = 'O'
            data = {
                'first_name': user_data.get('name', '').split()[0],
                'last_name': user_data.get('family_name'),
                'google_avatar': user_data.get('picture'),
                'gender': gender,
                'is_active': True
            }
            user.__dict__.update(data)
            user.save()
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)
        else:
            messages.error(
                request,
                'Unable to login with Gmail Please try again'
            )
        return redirect('booking')
    else:
        url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
        scope = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        scope = " ".join(scope)
        url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
        return redirect(url)

## Reviews

def format_sentence(sent):
    return({word: True for word in nltk.word_tokenize(sent)})
@login_required
def reviewViews(request):
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            comment = form.cleaned_data['comment']

            # give prediction response review_model.pkl
            loaded_model = pickle.load(
                open("hotel_app/review_model.pkl", 'rb')) ## Change this to base dir. 
            ratings = loaded_model.classify(format_sentence(comment))
            form.instance.guest_ID = request.user
            form.instance.rating = loaded_model.classify(format_sentence(comment))
            form.save()
            #return render(request, 'review.html', {'form': form, 'ratings': ratings}) 
            return redirect('home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form})

def paymentView(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_owner = form.cleaned_data['card_owner']
            card_number = form.cleaned_data['card_number']
            card_cvv = form.cleaned_data['card_cvv']
            exp_month = form.cleaned_data['exp_month']
            exp_year = form.cleaned_data['exp_year']
            form.instance.booking_num = Booking.objects.filter(guest_ID=request.user).last()
            form.save()
            return redirect('receipt')
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {'form': form})


class RoomsLists(ListView):
    model = Room
    template_name = "booking-noauth.html"
    
    def get_context_data(self, **kwargs):
        content = super(RoomsLists, self).get_context_data(**kwargs)
        content['rooms'] = Room.objects.filter(is_available=True)
        return content 
