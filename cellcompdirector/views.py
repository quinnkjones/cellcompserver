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

@require_http_methods(["GET"])
def home(request):
    return render(request,'home.html')

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

def cma(An,xn1,n):
    return (xn1+float(n*An))/(n+1)


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

@require_http_methods(['GET'])
@login_required(redirect_field_name = 'cellcomp:home')
def checkSuper(request):
    if not request.user.is_superuser:
        return redirect('cellcomp:newsession')
    else:
        return render_to_response('adminfunctions.html')



def genIndexDict():
    index = 0
    indices = {}
    for c in Cell.objects.all():
        indices[c.cellID] = index
        index += 1
    return indices

def dumpFile(fname):
    fullpath = settings.STATIC_ROOT+'dump/'+fname


    #create master model
    numCells = Cell.objects.count()
    model = np.zeros((numCells,numCells))

    indices = genIndexDict()

    #add to master model with normalized ratings
    for u in Rater.objects.all():
        mean = u.mean()
        #TODO take trust measure into account here
        for r in u.ratings().all():
            normR = r.rating-mean
            row = indices[r.controlCell.cellID]
            col = indices[r.variableCell.cellID]

            model[row,col] += normR

    np.save(fullpath,model)



    return 'dump/'+fname+'.npy'

def dumpRaw(fname):
    fullpath = settings.STATIC_ROOT+'dump/'+fname


    #create master model
    numCells = Cell.objects.count()
    numRaters = Rater.objects.count()
    model = np.zeros((numRaters,numCells,numCells))

    indices = genIndexDict()

    depth = 0
    for u in Rater.objects.all():
        for r in u.ratings().all():
            row = indices[r.controlCell.cellID]
            col = indices[r.variableCell.cellID]

            model[depth,row,col] = r.rating

        depth += 1

    np.save(fullpath,model)



    return 'dump/'+fname+'.npy'


@require_http_methods(['GET'])
@login_required(redirect_field_name='cellcomp:home')
def datadump(request, method):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Only Admin Site Members have access to this page')
    else:
        fname = strftime("%a-%d-%b-%Y-%H-%M-%S", gmtime())

        if method == 'accumulatedMean':
            subfolder = dumpFile(fname)
        elif method == 'raw':
            subfolder = dumpRaw(fname)
        else:
            return HttpResponseNotAllowed('must have an acceptable method in url')
        return redirect(settings.STATIC_URL + '/' + subfolder)
