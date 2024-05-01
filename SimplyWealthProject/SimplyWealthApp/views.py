from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignupForm, ProfilePictureForm, FriendSearchForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.utils import timezone
from django.db.models import Sum
import decimal
import uuid 
from os.path import splitext
from datetime import date, datetime, timedelta
import requests
import json


def index(request):
    return render(request, "welcome/index.html")

def sell_stock(request):
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        params = json.loads(request.body.decode('utf-8'))
        user_account = Transaction.objects.get(user=user_profile)
        user_stock_portfolio = UserStockPortfolio.objects.filter(user = user_profile, stock_symbol=params['stock_symbol'])
        if len(user_stock_portfolio) == 0:
            return JsonResponse({"response_code":402, "msg":"Stock not found in User Portfolio."})
        else:
            for record in user_stock_portfolio:
                if float(record.stock_units) >= float(params['stock_units']):
                    record.stock_units = float(record.stock_units) - float(params['stock_units'])
                    record.save()
                else:
                    return JsonResponse({"response_code":403, "msg":"Selected number of stock units is greater than avaible stock units in user portfolio."})
        user_amount = user_account.amount
        stock_sell_amount = params['stock_price'] * params['stock_units']
        uuid_str = uuid.uuid4()
        print(uuid_str)
        stock_transanction = StockTransanctions(user=user_profile, transaction_id=uuid_str, stock_symbol=params['stock_symbol'], 
                                                    transaction_type='sell',stock_price = params['stock_price'], stock_price_date = params['stock_price_date'], stock_units=params['stock_units'], timestamp=timezone.now())
        stock_transanction.save()
        user_amount = float(user_amount) + float(stock_sell_amount)
        user_account.amount = round(user_amount, 2)
        user_account.save()
        return JsonResponse({"response_code":200, "msg":"Successfully sold stock units."})
        

def buy_stock(request):
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        params = json.loads(request.body.decode('utf-8'))
        user_account = Transaction.objects.get(user=user_profile)
        user_amount = float(user_account.amount)
        stock_buy_amount = float(params['stock_price'] * params['stock_units'])
        if stock_buy_amount < user_amount:
            uuid_str = uuid.uuid4()
            print(uuid_str)
            stock_transanction = StockTransanctions(user=user_profile, transaction_id=uuid_str, stock_symbol=params['stock_symbol'], 
                                                    transaction_type='buy',stock_price = params['stock_price'], stock_price_date = params['stock_price_date'], stock_units=params['stock_units'], timestamp=timezone.now())
            stock_transanction.save()
            user_amount = float(user_amount) - float(stock_buy_amount)
            user_account.amount = round(user_amount, 2)
            user_account.save()
            user_stock_portfolio = UserStockPortfolio.objects.filter(user = user_profile, stock_symbol=params['stock_symbol'])
            if len(user_stock_portfolio) == 0:
                portfolio_update = UserStockPortfolio(user = user_profile, stock_symbol=params['stock_symbol'], stock_units = params['stock_units'])
                portfolio_update.save()
                return JsonResponse({"response_code":200, "msg":"New stock successfully purchased."})
            else:
                for record in user_stock_portfolio:
                    record.stock_units = float(record.stock_units) + float(params['stock_units'])
                    record.save()
                return JsonResponse({"response_code":200, "msg":"Stock Units updated with new purchased quantity."})
        else:
            return JsonResponse({"response_code":401, "msg":"Amount not enough to buy the number of stock units selected."})

def get_stock_units(request):
    if request.method == "GET":
        user_profile = UserProfile.objects.get(user=request.user)
        
        user_stock_portfolio = UserStockPortfolio.objects.filter(user = user_profile, stock_symbol=request.GET.get('stock_symbol'))
        print(user_stock_portfolio)
        if len(user_stock_portfolio) == 0:
            return JsonResponse({"msg":"Stock not found", "stock_units":0})
        else:
            for record in user_stock_portfolio:
                return JsonResponse({"msg":"Stock found", "stock_units":record.stock_units})

def get_ticker_details(request):
    if request.method == "POST":
        form = request.POST
        # if form.is_valid():
        try:
            stock_name = form.get('stockName').strip().upper()
            ticker_details_endpoint_url = f"https://api.polygon.io/v3/reference/tickers/{stock_name}?apiKey=UqR1AwHB4eIRO0pUzjG8IxuMlFHeJczI"
            response = requests.get(ticker_details_endpoint_url).json()
            
            output_response = {'results':json.dumps(response['results'])}
            user_profile = UserProfile.objects.get(user=request.user)
            user_stock_portfolio = UserStockPortfolio.objects.filter(user = user_profile, stock_symbol=stock_name)
            for record in user_stock_portfolio:
                if record.stock_units > 0:
                    output_response['sell_option'] = True
                else:
                    output_response['sell_option'] = False
                
            curr_date =  date.today()
            thirty_days_ago = curr_date - timedelta(days=30)

            ticker_timeseries_endpoint_url = f"https://api.polygon.io/v2/aggs/ticker/{stock_name}/range/1/day/{thirty_days_ago}/{curr_date}?adjusted=true&sort=desc&limit=30&apiKey=UqR1AwHB4eIRO0pUzjG8IxuMlFHeJczI"
            time_series_response = requests.get(ticker_timeseries_endpoint_url).json()['results']
            for val in time_series_response:
                val['t']=datetime.fromtimestamp(val['t']/1000).strftime('%Y-%m-%d')
            latest_stock_price = time_series_response[0]
            time_series_response = time_series_response[::-1]
            
            output_response['time_series'] = json.dumps(time_series_response)
            output_response['latest_stock_price'] = json.dumps(latest_stock_price)
            return render(request, 'user/tickerDetails.html', output_response)
        except Exception:
            return render(request, "misc/notfound_page.html")


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
            return render(request, "misc/notfound_page.html")
    else:
        form = SignupForm()
        context = {'form': form}
        return render(request, "welcome/signup.html", context)

def logout_view(request):
    logout(request)
    return render(request, "welcome/index.html")

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

            # Fetch data for top gainers
            top_gainers_data = TopDailyGainers.objects.order_by('-insert_time')[:5]

            # Fetch data for top movers
            top_movers_data = MostActivelyTraded.objects.order_by('-insert_time')[:5]

            # Fetch data for 
            top_losers_data = TopDailyLosers.objects.order_by('-insert_time')[:5]

            # Fetch data for 
            leader_board = Leaderboard_Weekly.objects.order_by('-current_total')[:5]
            user_portfolio = UserStockPortfolio.objects.filter(user=user_profile, stock_units__gt = 0)
            curr_date =  date.today()
            user_portfolio_perfomance = {"dates":[], 'stocks':{'portfolio':[]}}
            user_stocks = dict()
            for instance in user_portfolio:
                user_stocks[instance.stock_symbol] = instance.stock_units
            user_stock_prices = {'portfolio':None}
            date_iter = 1
            while len(user_portfolio_perfomance["dates"]) < 5:
                temp_date = curr_date - timedelta(days=date_iter)
                if temp_date.weekday() < 5:
                    user_portfolio_perfomance["dates"].append(temp_date.strftime('%Y-%m-%d'))
                date_iter += 1

            user_portfolio_perfomance["dates"] = user_portfolio_perfomance["dates"][::-1]

            user_stock_graph_data = dict()

            for user_stock, stock_units in user_stocks.items():
                api_url = f"https://api.polygon.io/v2/aggs/ticker/{user_stock}/range/1/day/{user_portfolio_perfomance['dates'][0]}/{user_portfolio_perfomance['dates'][-1]}?adjusted=true&sort=asc&apiKey=UqR1AwHB4eIRO0pUzjG8IxuMlFHeJczI"
                api_resp = requests.get(api_url).json()['results']
                user_stock_graph_data[user_stock] = [x['c'] for x in api_resp]

            
         
            if len(user_stocks) > 0:
                try:
                    for n in range(len(user_stocks)):
                        prev_day_portfol_price = user_stock_prices['portfolio']
                        curr_day_portfol_price = 0
                        for user_stock, stock_units in user_stocks.items():
                            if user_stock in user_stock_prices:
                                prev_day_price = user_stock_prices[user_stock]
                            else:
                                prev_day_price = None
                            temp_close_price = user_stock_graph_data[user_stock][n]
                            curr_day_portfol_price += temp_close_price
                            if prev_day_price is None:
                                profit_loss_percent = 0
                            else:
                                profit_loss_percent = ((temp_close_price - prev_day_price) / prev_day_price) * 100
                            if user_stock in user_portfolio_perfomance['stocks']:
                                user_portfolio_perfomance['stocks'][user_stock].append(profit_loss_percent)
                            else:
                                user_portfolio_perfomance['stocks'][user_stock] = [profit_loss_percent]
                            if user_stock in user_stock_prices:
                                pass
                            else:
                                user_stock_prices[user_stock] = temp_close_price
                        
                        if prev_day_portfol_price is None:
                            portfol_profit_losss_percent = 0
                        else:
                            portfol_profit_losss_percent = ((curr_day_portfol_price - prev_day_portfol_price)/prev_day_portfol_price) * 100
                        if user_stock_prices['portfolio'] is None:
                            user_stock_prices['portfolio'] = curr_day_portfol_price
                        user_portfolio_perfomance['stocks']['portfolio'].append(portfol_profit_losss_percent)
                except Exception as err:
                    user_portfolio_perfomance['stocks']['portfolio'] = [None, None, None, None, None]

            else:
                    user_portfolio_perfomance['stocks']['portfolio'] = [None, None, None, None, None]
                
            
            return render(request, "user/userhome.html", {'user_profile': user_profile, 
                                'user_total': total_amount, 
                                'top_gainers': top_gainers_data,
                                'top_movers': top_movers_data,
                                'top_losers': top_losers_data,
                                'leader_board': leader_board,
                                'user_portfolio_perfomance':json.dumps(user_portfolio_perfomance)})
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


def add_bio(request):
    if request.method == 'POST':
        text = request.POST.get('bio')
        # Assuming the user is logged in and you have access to the user object
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.text = text
        user_profile.save()
        return redirect('userhome')  # Redirect to profile view page
    else:
        return render(request, 'misc/notfound_page.html')  # Handle GET request


def leaderboard_users(request, user_id):
    try:
        # Fetch the user object based on the provided username
        user = User.objects.get(pk=user_id)
        # Assuming you have a UserProfile model associated with the User model
        user_profile = user.userprofile  # Replace 'userprofile' with your actual UserProfile model field name
        
        user_stock_portfolios = UserStockPortfolio.objects.filter(user=user_profile)
        context = {
            'user': user,
            'user_profile': user_profile,
            'stocks':user_stock_portfolios
            }
        return render(request, 'user/leaderboard_users.html', context)
    except Exception:
        # Handle the case where the user does not exist
        return render(request, 'misc/hidden_user.html')


def company_info(request):
    return render(request, 'misc/company_info.html')

def info(request):
    return render(request, 'misc/info.html')

def contact(request):
    return render(request, 'misc/contact.html')


def search_friends(request):
    query = request.GET.get('query')
    if query:
        # Perform a search based on the query
        user = User.objects.get(username=query)
        # Assuming you have a UserProfile model associated with the User model
        try:
            user_profile = user.userprofile  # Replace 'userprofile' with your actual UserProfile model field name
        except Exception as err:
            return render(request, 'misc/hidden_user.html')

        user_stock_portfolios = UserStockPortfolio.objects.filter(user=user_profile)
        context = {
            'user': user,
            'user_profile': user_profile,
            'stocks':user_stock_portfolios
            }
        return render(request, 'user/leaderboard_users.html', context)
    else:
        # If no query is provided, return all friends
        friends = User.objects.all()
    return render(request, 'leaderboard_users.html', {'friends': friends, 'query': query})

# from django.http import JsonResponse

# # def fetch_populated_data(request):
# #     print("HELLLLLO")
    
# #     # Define fake data for debugging
# #     fake_data = [
# #         {"ticker": "AAPL", "price": 150.00, "change_amount": 2.50, "change_percentage": 1.5},
# #         {"ticker": "GOOGL", "price": 2500.00, "change_amount": -10.50, "change_percentage": -0.5},
# #         {"ticker": "MSFT", "price": 300.00, "change_amount": 5.00, "change_percentage": 2.0},
# #         {"ticker": "AMZN", "price": 3500.00, "change_amount": -20.00, "change_percentage": -0.7},
# #         {"ticker": "FB", "price": 300.00, "change_amount": 3.00, "change_percentage": 1.0},
# #     ]
    
# #     return JsonResponse({'data': fake_data})



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
