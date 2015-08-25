from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
import datetime
# Create your views here.

@require_http_methods(["GET"])
def home(request):
    return render(request,'home.html')

@require_http_methods(["GET"])
def playCellComp(request):
    #t = get_template('play.html')
    c = {}
    #c.update(csrf(request))
    c['leftcell'] = '~/left' #TODO replace with the code that picks the correct cell
    c['rightcell'] = '~/right' #TODO see above
    #TODO decide on a cell selection strategy
    #TODO find an appropriate way to store the volatile info about what cells each indiviual user is looking at
    print c
    return render_to_response('play.html',c,context_instance=RequestContext(request))

@require_http_methods(["POST"])
def addNewRating(request):
    print request.POST['rating']
    #TODO add rating into system
    return redirect('cellcomp:play')
