from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "welcome/index.html")


## SIGNUP AND LOGIN _ ACCOUNTS PAGE
def signup(request):
    return render(request, "welcome/signup.html")


###
def userhome(request, username):
    return HttpResponse(f"{username}'s homepage!")


