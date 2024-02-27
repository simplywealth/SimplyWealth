from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignupForm, ProfilePictureForm
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import UserProfile, Transaction
from django.utils import timezone
from django.db.models import Sum

import uuid 
from os.path import splitext
from datetime import date, datetime, timedelta
import requests
import json


def index(request):
    return render(request, "welcome/index.html")


def get_ticker_details(request):
    if request.method == "POST":
        form = request.POST
        # if form.is_valid():
        stock_name = form.get('stockName').strip().upper()
        ticker_details_endpoint_url = f"https://api.polygon.io/v3/reference/tickers/{stock_name}?apiKey=LnR21zv6euM7KmY_HafxN9XgwdnmltXE"
        response = requests.get(ticker_details_endpoint_url).json()
        output_response = {'results':response['results']}
        curr_date =  date.today()
        thirty_days_ago = curr_date - timedelta(days=30)

        ticker_timeseries_endpoint_url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/{thirty_days_ago}/{curr_date}?adjusted=true&sort=asc&limit=30&apiKey=LnR21zv6euM7KmY_HafxN9XgwdnmltXE"
        time_series_response = requests.get(ticker_timeseries_endpoint_url).json()['results']
        for val in time_series_response:
            val['t']=datetime.fromtimestamp(val['t']/1000).strftime('%Y-%m-%d')
        output_response['time_series'] = json.dumps(time_series_response)
        return render(request, 'user/tickerDetails.html', output_response)






## SIGNUP AND LOGIN - ACCOUNTS PAGE
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active = True 
            user.save() 

            # create userprofile for the newly created user
            profile=UserProfile.objects.create(user=user)

            #create transaction record for the new user 
            Transaction.objects.create(transaction_id= uuid.uuid4(), user=profile, amount=1000, timestamp=timezone.now())

            messages.success(request, "Thank you for signing up!\n You should receive a confirmation email shortly.")
            return render(request, 'welcome/signup/success.html')
        else:
            error_messages = form.errors.values()
            for error_list in error_messages:
                for error in error_list:
                    messages.error(request, error)
            return render(request, "welcome/signup.html", {'form': form})
    else:
        form = SignupForm()
        context = {'form': form}
        return render(request, "welcome/signup.html", context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print('here')
            if user is not None:
                print('here')
                login(request, user)
                return redirect(reverse('userhome'))
        else:
            return render(request, "welcome/signup.html", {'form': form})
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, "welcome/login.html", context)
###
def calculate_total(user_transactions):
    return user_transactions.aggregate(total=Sum('amount'))['total']

def userhome(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_transactions = Transaction.objects.filter(user=user_profile)
            total_amount= calculate_total(user_transactions)
            return render(request, "user/userhome.html", {'user_profile': user_profile, 'user_total': total_amount})
        except UserProfile.DoesNotExist:
            messages.error(request, "user profile not found.")
            return redirect('index')
    else:
        messages.error(request, "please login first.")
        return redirect('login_view')
#    return render(request, "user/userhome.html", {'username':request.user})


def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            unique_filename = str(uuid.uuid4()) + splitext(request.FILES['profile_picture'].name)[1]
            
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.profile_picture.save(unique_filename, request.FILES['profile_picture'])
            user_profile.save()
            return redirect('userhome')  # Redirect to user's home page or any other page
    else:
        form = ProfilePictureForm()
    return render(request, 'upload_profile_picture.html', {'form': form})


def test_charjs(request):
    return render(request, "user/testchartjs.html")
    
    
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='user/testchartjs.html')
line_chart_json = LineChartJSONView.as_view()