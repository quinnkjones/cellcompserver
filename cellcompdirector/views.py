from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import datetime
from cellcompdirector.models import *
# Create your views here.

@require_http_methods(["GET"])
def home(request):
    return render(request,'home.html')

@require_http_methods(["GET"])
@login_required(redirect_field_name='cellcomp:home')
def playCellComp(request):
    #t = get_template('play.html')
    c = {}
    #c.update(csrf(request))
    rater = Rater.objects.get(user=request.user)
    leftcell,rightcell = rater.nextCellPair()
    c['leftcell'] = leftcell
    c['rightcell'] = rightcell

    #TODO find an appropriate way to store the volatile info about what cells each indiviual user is looking at
        #have hirsh's code send it as well?
    print c
    return render_to_response('play.html',c,context_instance=RequestContext(request))



@require_http_methods(["POST"])
@login_required(redirect_field_name='cellcomp:home')
def addNewRating(request):
    print request.POST['rating']
    #TODO add rating into system
    return redirect('cellcomp:play')
