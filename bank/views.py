from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import random
from .models import User, StockPortfolio, Transactions
from django.contrib.auth.decorators import login_required
import requests
import os




def login_view(request):
    if request.method == "POST": 

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bank/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bank/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        account_number = str(random.randint(1, 999999999999)) 

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "bank/register.html", {
                "message": "Passwords must match."
            })

                # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.account_number = account_number
            user.save()
        except IntegrityError:
            return render(request, "bank/register.html", {
                "message": "Username already taken."
            })
 

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "bank/register.html")


def index(request):

    if request.user.is_authenticated:
        user= request.user
        usd_account = user.usd_account
        eur_account = user.eur_account
        transactions = user.transactions.all().order_by('-timestamp')[:5]

        return render(request, "bank/index.html",{'usd_account': usd_account,
                                                   'eur_account': eur_account,
                                                   'transactions': transactions})

    else:
        return  HttpResponseRedirect(reverse('login'))


@login_required
def deposit(request):

    if request.method == "GET":
        return render(request, "bank/deposit.html") 
    
    if request.method == "POST":
        new_deposit= float(request.POST.get('new_deposit'))
        user = request.user 
        usd_account = float(user.usd_account)
        usd_account += new_deposit
        user.usd_account = usd_account
        user.save()

        new_transaction = Transactions(user=user, description = f"Deposit of USD {new_deposit}")
        new_transaction.save()

        message = f"You have successfully deposited USD {new_deposit}!" 

        return render(request, "bank/deposit.html", {'message': message}) 
    

@login_required
def withdraw(request):

    if request.method == "GET":
        return render(request, "bank/withdraw.html") 
    
    if request.method == "POST":
        new_withdraw= float(request.POST.get('new_withdraw'))
        user = request.user 
        usd_account = float(user.usd_account)

        if new_withdraw > usd_account:
            message = "Insufficient funds!"
            return render(request, "bank/withdraw.html", {'message': message}) 
        
        usd_account -= new_withdraw
        user.usd_account = usd_account
        user.save()

        new_transaction = Transactions(user=user, description = f"Withdraw of USD {new_withdraw}")
        new_transaction.save()

        message = f"You have successfully withdrew USD {new_withdraw}!" 

        return render(request, "bank/withdraw.html", {'message': message}) 


@login_required
def transfer(request):

    user = request.user 
    usd_account = user.usd_account
    account_number = user.account_number

    if request.method == "GET":     
        
        return render(request, "bank/transfer.html", 
                      {'account_number': account_number, 
                       'usd_account': usd_account}) 
    
    if request.method == "POST":
        account_number_receiver= request.POST.get('transfer-receiver')
        amount= float(request.POST.get('transfer-amount'))

        if amount > usd_account:
            message = "Insufficient funds!"
            return render(request, "bank/transfer.html", 
                          {'message': message,
                           'account_number': account_number,
                           'usd_account': usd_account
                           }) 
        

        user.usd_account = float(user.usd_account) - amount
        user.save()

        receiver = User.objects.get(account_number=account_number_receiver)
        receiver.usd_account = float(receiver.usd_account) + amount
        receiver.save()

        new_transaction = Transactions(user=user, description = f"Transfer of USD {amount} to {receiver.username}")
        new_transaction.save()

        new_transaction_2 = Transactions(user=receiver, description = f"Transfer of USD {amount} from {user.username}")
        new_transaction_2.save()

        message = f"You have successfully transfered USD {amount} to {receiver.username}!" 

        return render(request, "bank/transfer.html", 
                      {'account_number': account_number, 
                       'usd_account': usd_account,
                       'message': message})  
    

@login_required
def get_name(request, receiver_account_number):
    
    try:
        receiver = User.objects.get(account_number=receiver_account_number)
        return JsonResponse({'name': f"{receiver.first_name} {receiver.last_name}"})  
    except User.DoesNotExist:
        return JsonResponse({'name': None})  

@login_required    
def get_eur_price(request):
    api_key = os.getenv('API_KEY')
    url = f"https://api.exchangeratesapi.io/latest?access_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "Error"}, status=500)    

@login_required
def eur_exchange(request):

    user = request.user 
    usd_account = user.usd_account
    eur_account = user.eur_account

    if request.method == "GET":     
        
        return render(request, "bank/eur_exchange.html", 
                      {'eur_account': eur_account, 
                       'usd_account': usd_account}) 

    if request.method == "POST":
        
        try:
            rate = float(request.POST.get('exchange_rate_hidden'))
            amount_to_convert= float(request.POST.get('amount'))
        except ValueError:
            message = "Quotation or amount not found!"
            return render(request, "bank/eur_exchange.html", 
                          {'message': message,
                           'eur_account': eur_account,
                           'usd_account': usd_account
                           })

        currency = request.POST.get('currency')

        if currency == "USDtoEUR":

            if amount_to_convert > usd_account:
                message = "Insufficient funds!"
                return render(request, "bank/eur_exchange.html", 
                            {'message': message,
                            'eur_account': eur_account,
                            'usd_account': usd_account
                            }) 

            EUR_amount = amount_to_convert/rate
            user.usd_account = float(usd_account) - amount_to_convert
            user.eur_account = float(eur_account) + EUR_amount
            user.save()

            new_transaction = Transactions(user=user, description = f"USD {amount_to_convert} converted to EUR")
            new_transaction.save()

            return  HttpResponseRedirect(reverse('index'))     

        elif currency == "EURtoUSD":

            if amount_to_convert > eur_account:
                message = "Insufficient funds!"
                return render(request, "bank/eur_exchange.html", 
                            {'message': message,
                            'eur_account': eur_account,
                            'usd_account': usd_account
                            }) 

            USD_amount = amount_to_convert*rate
            user.eur_account = float(eur_account) - amount_to_convert
            user.usd_account = float(usd_account) + USD_amount
            user.save()

            new_transaction = Transactions(user=user, description = f"EUR {amount_to_convert} converted to USD")
            new_transaction.save()

            return  HttpResponseRedirect(reverse('index'))   

        else:
            message = "Select currency to convert!"
            return render(request, "bank/eur_exchange.html", 
                        {'message': message,
                        'eur_account': eur_account,
                        'usd_account': usd_account
                        })  


def get_stock_price(request, symbol):  

    if symbol == "KO":  
        price = str(round(random.uniform(55.0, 65.0), 2))

    elif symbol == "GOOGL":  
        price = str(round(random.uniform(130.0, 140.0), 2))

    elif symbol == "AAPL":  
        price = str(round(random.uniform(170.0, 180.0), 2)) 

    elif symbol == "MSFT":  
        price = str(round(random.uniform(300.0, 310.0), 2))   

    elif symbol == "AMZN":  
        price = str(round(random.uniform(130.0, 140.0), 2)) 

    elif symbol == "NVDA":  
        price = str(round(random.uniform(430.0, 500.0), 2))                                

    return JsonResponse({
        "price": price,
        "symbol": symbol
    })                      


@login_required
def stocks(request):

    user = request.user 
    usd_account = user.usd_account

    if request.method == "GET":    

        portfolios = user.portfolios.all() 
        
        return render(request, "bank/stocks.html", 
                      {'usd_account': usd_account,
                       'portfolios': portfolios}) 
    
    if request.method == "POST": 

        try:
            shares= int(request.POST.get('stock-shares'))
            price= float(request.POST.get('stock-price'))
            side= request.POST.get('side')
            stock_symbol = request.POST.get('stock-symbol')

        except ValueError:    

                message = "Missing data!"
                portfolios = user.portfolios.all()  

                return render(request, "bank/stocks.html", {'message': message,
                                                            'portfolios': portfolios,
                                                            'usd_account': usd_account})

        if side == "buy":

            if (shares * price) > float(usd_account):

                message = "Insufficient funds!"
                portfolios = user.portfolios.all()  

                return render(request, "bank/stocks.html", {'message': message,
                                                            'portfolios': portfolios,
                                                            'usd_account': usd_account})
            
            else:

                user.usd_account = float(usd_account) - shares * price
                user.save()

                try:
                    portfolio_item = StockPortfolio.objects.get(user=user, stock_symbol=stock_symbol)
                    portfolio_item.quantity += shares
                    portfolio_item.purchase_price = price
                    portfolio_item.save()
                except StockPortfolio.DoesNotExist:
                    portfolio_item = StockPortfolio(user=user, stock_symbol=stock_symbol, quantity=shares, purchase_price=price)  
                    portfolio_item.save() 


                message = f"You have successfully bought {shares} shares of {stock_symbol}!"
                portfolios = user.portfolios.all()  
                new_transaction = Transactions(user=user, description = f"Purchase of {shares} {stock_symbol} shares for a total amount of USD {shares * price}")
                new_transaction.save()

                return render(request, "bank/stocks.html", {'message': message,
                                                            'portfolios': portfolios,
                                                            'usd_account': usd_account}) 

        if side == "sell": 

            try:
                portfolio_item = StockPortfolio.objects.get(user=user, stock_symbol=stock_symbol)

                if shares > portfolio_item.quantity:

                    message = "Not enought shares" 
                    portfolios = user.portfolios.all()  

                    return render(request, "bank/stocks.html", {'message': message,
                                                                'portfolios': portfolios,
                                                                'usd_account': usd_account}) 
                
                portfolio_item.quantity -= shares
                portfolio_item.save()
                user.usd_account = float(usd_account) + shares * price
                user.save()

                message = f"You have successfully sold {shares} shares of {stock_symbol}!"
                portfolios = user.portfolios.all()  

                new_transaction = Transactions(user=user, description = f"Sell of {shares} {stock_symbol} shares for a total amount of USD {shares * price}")
                new_transaction.save()

                return render(request, "bank/stocks.html", {'message': message,
                                                            'portfolios': portfolios,
                                                            'usd_account': usd_account}) 

            except StockPortfolio.DoesNotExist:

                message = f"You do not own {stock_symbol} shares in your portfolio" 
                portfolios = user.portfolios.all()  

                return render(request, "bank/stocks.html", {'message': message,
                                                            'portfolios': portfolios,
                                                            'usd_account': usd_account})
            



@login_required
def history(request):

    user = request.user 

    if request.method == "GET":    

        transactions = user.transactions.all().order_by('-timestamp')
        
        return render(request, "bank/history.html", {'transactions': transactions})             



