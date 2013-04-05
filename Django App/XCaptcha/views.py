from django.shortcuts import render_to_response, redirect
from models import CaptchaTestForm
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

@csrf_exempt
def form(request):
    if request.POST:
        form = CaptchaTestForm(request.POST)
        
        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():
            human = True
            return HttpResponseRedirect('/success/')
    else:
        form = CaptchaTestForm()
    return render_to_response('template.html',locals())

def success(request):
    return render_to_response('success.html')