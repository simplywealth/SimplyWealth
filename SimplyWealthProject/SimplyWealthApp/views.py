from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, "welcome/index.html")


## SIGNUP AND LOGIN - ACCOUNTS PAGE
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for signing up!\n You should receive a confirmation email shortly.")
            return render(request, 'welcome/signup/success.html')
        else:
            print("Form Validation Errors:", form.errors)  # Print form validation errors
            print("NOT VALID FORM")
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
            if user is not None:
                login(request, user)
                return(redirect('index'))
        else:
            return render(request, "welcome/signup.html", {'form': form})
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, "welcome/login.html", context)
###
def userhome(request, username):
    return HttpResponse(f"{username}'s homepage!")


# def registerPage(request):
#     form = UserCreationForm()
#     context = {'form':form}
#     return render(request, 'welcome/register.html', UserCreationForm())