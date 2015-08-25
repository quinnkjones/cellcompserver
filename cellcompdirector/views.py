from django.shortcuts import render
from django.http import HttpResponse
from cellcompdirector.models import User
from django.views.decorators.http import require_http_methods
import datetime
# Create your views here.

@require_http_methods(["GET"])
def home(request):
    return render(request,'home.html')

@require_http_methods(["GET"])
def playCellComp(request):
    return HttpResponse("pass")

@require_http_methods(["POST"])
def addNewRating(request):
    return HttpResponse("pass")
