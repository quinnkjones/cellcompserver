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

from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect

@require_http_methods(["GET"])
def home(request):
    return render(request,'home.html')

def cma(An,xn1,n):
    return (xn1+float(n*An))/(n+1)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            rater = Rater(user = user,name = user.username)
            rater.save()
            print rater
            return redirect('cellcomp:loginpage')
    else:
        form = UserCreateForm()
    return render_to_response("registration/register.html",{'form': form},context_instance=RequestContext(request))

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



@require_http_methods(['GET','POST'])
def resetPasswordRequest(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST['addr'])
        except DoesNotExist:
            return redirect('cellcomp:loginpage')

        subject = "Recovery Email for WVU-SNRC CellComp"

        to = [user.email]
        from_email = 'quinnkjones@gmail.com'

        ctx = {
            'user': user
        }

        message = get_template('main/email/email.html').render(Context(ctx))
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

        return HttpResponse('email_two')
    else:
        pass
