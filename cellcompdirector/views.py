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
    request.session['cellpair'] = (leftcell.cellID,rightcell.cellID)
    print c
    return render_to_response('play.html',c,context_instance=RequestContext(request))

@require_http_methods(['GET'])
@login_required(redirect_field_name = 'cellcomp:home')
def checkSuper(request):
    if not request.user.is_superuser:
        return redirect('cellcomp:play')
    else:
        return render_to_response('adminfunctions.html')

@require_http_methods(["POST"])
@login_required(redirect_field_name='cellcomp:home')
def addNewRating(request):
    ratingNum =  request.POST['rating']
    leftcid,rightcid =  request.session['cellpair']
    leftcell = Cell.objects.get(cellID = leftcid)
    rightcell = Cell.objects.get(cellID = rightcid)
    rater = Rater.objects.get(user = request.user)
    rating = Rating(controlCell = leftcell,variableCell = rightcell,user = rater, rating = ratingNum)
    rating.save()
    return redirect('cellcomp:play')

def genIndexDict():
    index = 0
    indices = {}
    for c in Cell.objects.all():
        indices[c.cellID] = index
        index += 1
    return indices

def dumpFile(fname):
    fullpath = settings.STATIC_ROOT+'dump/'+fname
    #TODO perform user rating normalization combine into master rating grid output to file download

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
    #TODO perform user rating normalization combine into master rating grid output to file download

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
