"""sys_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# import from views hotelapp
from hotel_app.views import home_view, receipt_view
# views related sa accounts login and creation 
from hotel_app.views import login_view, logout_view, register_view
# Class views related sa booking and booklist ng guest 
from hotel_app.views import BookingView, BookingListView, RoomsLists
# views contact form  && google && reviews
from hotel_app.views import contactView, google_login, reviewViews, paymentView
##Image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('', home_view, name='home'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('availablerooms/', RoomsLists.as_view(), name='availablerooms'), 
    path('bookinglist/', BookingListView.as_view(), name='bookinglist'),
    path('receipt/', receipt_view, name='receipt'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('contact/', contactView, name='contact'),
    path('google_login', google_login, name="google_login"),
    path('review', reviewViews, name="review"),
    path('payment/', paymentView, name="payment"),

]

admin.site.site_header = 'BetterSogo: Staff Page'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)