from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from time import gmtime, strftime
from django.http import *
from cellcompdirector.models import *
from django.conf import settings
from struct import pack
import numpy as np
from django.views.decorators.csrf import csrf_exempt

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect

def parsetime(tstring):
    try:
        t = time.strptime(tstring,'%Mm')
    except ValueError:
        try:
            t = time.strptime(tstring,'%Ih%Mm')
        except ValueError:
            try:
                t = time.strptime(tstring,'%Ih')
            except ValueError:
                return None
    hour = t.tm_hour
    minutes = t.tm_min + hour*60
    secs = minutes*60
    return secs

@require_http_methods(['GET','POST'])
@login_required(redirect_field_name='cellcomp:home')
def sessionEnd(request):
    if request.method == 'GET':
        rater = Rater.objects.get(user = request.user)
        sessobj = SessionInfo(rater,request.request.session['sessionAvg'],request.session['sessionCount'])
        sessobj.save() #TODO finish saving session rates
        sessions =  SessionInfo.objects.filter(user = rater)

        return render_to_response('sessionEnd.html',{'failed':False},context_instance=RequestContext(request))
    else:
        tstring = request.POST['time']
        secs = parsetime(tstring)
        if secs is None:

            return render_to_response('sessionEnd.html',{'failed':True},context_instance=RequestContext(request))
        request.session['sessioncountdown'] = secs
        request.session['pretime'] = time.time()
        request.session['controlCell'] = 0
        return redirect('cellcomp:play')

@require_http_methods(['GET','POST'])
@login_required(redirect_field_name='cellcomp:home')
def sessionStart(request):
    if request.method == 'GET':
        return render_to_response('sessionStart.html',{'failed':False},context_instance=RequestContext(request))
    else:
        #tstring = request.POST['time']
        #secs = parsetime(tstring)
        try:
            controlNumber = int(request.POST['goal'])
        except ValueError as e:
            return render_to_response('sessionStart.html',{'failed':True},context_instance=RequestContext(request))

        #if secs is None:
        #    return render_to_response('sessionStart.html',{'failed':True},context_instance=RequestContext(request))
        #request.session['sessioncountdown'] = secs
        request.session['cellGoal'] = controlNumber
        request.session['pretime'] = time.time()
        request.session['controlCell'] = 0
        request.session['sessionAvg'] = 0
        request.session['sessionCount'] = 0
        return redirect('cellcomp:play')

def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

def sessionExpired(request):
    return request.session['cellGoal'] == 0#request.session['sessioncountdown'] <= 0 or time.time()-request.session['pretime'] >= settings.SESSION_CUSTOM_TIMEOUT

@require_http_methods(["GET"])
@login_required(redirect_field_name='cellcomp:home')
def playCellComp(request):
    if sessionExpired(request):
        return redirect('cellcomp:home')
    #t = get_template('play.html')
    c = {}
    #c.update(csrf(request))
    rater = Rater.objects.get(user=request.user)


    print request.session['controlCell']
    try:
        (leftcell,rightcell),newControl = rater.nextCellPair(cCell = get_or_none(Cell,cellID = request.session.get('controlCell',0)))
    except PermuteTimeoutError, e:
        print e.value
        return redirect('cellcomp:home')

    c['leftcell'] = leftcell
    if newControl:
        request.session['cellGoal'] -= 1
        request.session['controlCell'] = leftcell.cellID
    c['rightcell'] = rightcell
    #c['timeleft'] = request.session['sessioncountdown']
    request.session['cellpair'] = (leftcell.cellID,rightcell.cellID)
    request.session['pretime'] = time.time()
    print c
    return render_to_response('play.html',c,context_instance=RequestContext(request))

@require_http_methods(["POST"])
@login_required(redirect_field_name='cellcomp:home')
def addNewRating(request):

    postTime = time.time()
    diff = postTime - request.session['pretime']

    #request.session['sessioncountdown'] = request.session['sessioncountdown']-diff

    ratingNum =  request.POST['rating']
    leftcid,rightcid =  request.session['cellpair']
    leftcell = Cell.objects.get(cellID = leftcid)
    rightcell = Cell.objects.get(cellID = rightcid)
    rater = Rater.objects.get(user = request.user)
    rater.ratingRateAvg = cma(rater.ratingRateAvg,diff,rater.ratingCount)
    print rater.ratingRateAvg
    rater.ratingCount += 1
    rater.save()
    request.session['sessionAvg'] = cma(request.session['sessionAvg'],diff,request.session['sessionCount'])
    request.session['sessionCount'] += 1
    rating,created = Rating.objects.get_or_create(controlCell = leftcell,variableCell = rightcell,user = rater,defaults = { 'rating' : ratingNum})
    if created:
        return redirect('cellcomp:play')
    else:
        return redirect('cellcomp:home')
