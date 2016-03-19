# ANT

from django.http import HttpRequest
from django.core.context_processors import request
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from ant.models import *
from django.conf import settings
from django.template.loader import render_to_string
import subprocess as sp
import os
import re
import json

import exercises

from django.forms.models import modelformset_factory
from django.views.decorators.csrf import ensure_csrf_cookie

# (Rev #32: #1)
from . import tasks
import celery

import sys
sys.stdout = sys.stderr


# (Rev #36: #1)
allowed_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
block_list = []


def index(request):
    '''
    Home page -- display the list of experiments
    '''
    #t = Theory.objects.all()
    # (Rev #36: #1)
    t = Theory.objects.filter(id__in = allowed_list)
    return render_to_response(
        'ant/home.html',
        {'theory': t},
        context_instance=RequestContext(request)
    )

def theory(request, object_id=9):
    # (Rev #36: #1)
    if object_id in block_list:
        return index(request)

    '''
    Theory for the selected experiment
    '''
#    print request.session.session_key
#    if 'key' in request.session:
#        print request.session['key']
#        request.session.set_expiry(0)
#    else:
#        request.session['key'] = 'Key'
#    return HttpResponse('Session')

    t = get_object_or_404(Theory, pk=object_id)
    t.content = t.content.replace('_STATIC_URL_', settings.STATIC_URL)
    context = RequestContext(request)
    # Required to differentiate between ISAD and ANT in post-comment.js
    context['SITE_BASE'] = '/cse28/ant/'
    t.content = t.content.replace('_STATIC_URL_', settings.STATIC_URL)

    return render_to_response(
        'ant/theory.html',
        {
            'object_id':    object_id,
            'theory':       t
        },
        context_instance=context
    )


def introduction(request, object_id=1):
    # (Rev #36: #1)
    if object_id in block_list:
        return index(request)

    t = get_object_or_404(Theory, pk=object_id)
    return render_to_response(
        'ant/introduction.html',
        {
            'title':        t.title,
            'introduction':    t.extra,
            'object_id':    object_id,
        },
        context_instance=RequestContext(request)
    )


def procedure(request, object_id=9):
    # (Rev #36: #1)
    if object_id in block_list:
        return index(request)

    # (Rev #42 : #1)
    #t = get_object_or_404(Theory, pk=object_id)
    p = get_object_or_404(Procedure.objects.select_related(), theory=object_id)
    p.content = p.content.replace('_STATIC_URL_', settings.STATIC_URL)
    return render_to_response(
        'ant/procedure.html',
        {
            'title':        p.theory.title,
            'procedure':    p.content,
            'object_id':    object_id,
        },
        context_instance=RequestContext(request)
    )

def simulation(request, object_id):
    # (Rev #36: #1)
    if object_id in block_list:
        return index(request)

    # (Rev #42 : #1)
    #t = get_object_or_404(Theory, pk=object_id)
    s = get_object_or_404(Simulation.objects.select_related(), theory=object_id)
    s.problem = s.problem.replace('_STATIC_URL_', settings.STATIC_URL)
    return render_to_response(
        'ant/simulation.html',
        {
            'title':        s.theory.title,
            'object_id':    object_id,
            'simulation':   s,
        },
        context_instance=RequestContext(request)
    )

def self_evaluation(request, object_id):
    # (Rev #36: #1)
    if object_id in block_list:
        return index(request)

    # (Rev #42 : #1)
    #t = get_object_or_404(Theory, pk=object_id)
    se = get_list_or_404(SelfEvaluation.objects.select_related(), theory=object_id)
    def ss(a, b):
        return (a.question_num - b.question_num)

    se.sort(key=lambda e: e.question_num)

    return render_to_response(
        'ant/sevaluation.html',
        {
            'title':        se[0].theory.title,
            'object_id':    object_id,
            'sevaluation':  se,
        },
        context_instance=RequestContext(request)
    )

def exercise(request, object_id):
    # (Rev #36: #1)
    if object_id in block_list:
        return index(request)

    # (Rev #42 : #1)
    #t = get_object_or_404(Theory, pk=object_id)
    e = get_list_or_404(Exercise.objects.select_related(), theory=object_id)
    return render_to_response(
        'ant/exercise.html',
        {
            'title':        e[0].theory.title,
            'object_id':    object_id,
            'exercise':     e,
        },
        context_instance=RequestContext(request)
    )

def references(request, object_id):
    # (Rev #36: #1)
    if object_id in block_list:
        return index(request)

    # (Rev #42 : #1)
    #t = get_object_or_404(Theory, pk=object_id)
    r = get_list_or_404(Reference.objects.select_related(), theory=object_id)
    return render_to_response(
        'ant/reference.html',
        {
        'title':        r[0].theory.title,
        'object_id':    object_id,
        'reference':    r
        },
        context_instance=RequestContext(request)
    )

def about_us(request):
    return render_to_response(
        'ant/about_us.html',
        {},
        context_instance=RequestContext(request)
    )

###def contact(request):
###    ContactFormSet = modelformset_factory(Contact, fields = ('name', 'email', 'website', 'organization', 'subject', 'comment',))
###    managementFormData = {
###        'form-TOTAL_FORMS':     u'1',
###        'form-INITIAL_FORMS':   u'0',
###        'form-MAX_NUM_FORMS':   u'1',
###        'form-0-title':         u'Contact',
###        'form-0-pub_date':      u'01 November 2010',
###    }
###    captcha_response = ''
###
###    if request.method == 'POST':                # The form has been already submitted
###        formSet = ContactFormSet(request.POST, managementFormData)  # A form bound tot he POST data
###        if formSet.is_valid():                  # All validation rules pass
###            # Process the data
###            name    = formSet.cleaned_data[0]['name']
###            email   = formSet.cleaned_data[0]['email']
###            website = formSet.cleaned_data[0]['website']
###            organization = formSet.cleaned_data[0]['organization']
###            subject = formSet.cleaned_data[0]['subject']
###            comment = formSet.cleaned_data[0]['comment']

###            # Talk to the reCAPTCHA service
###            response = captcha.submit(
###                request.POST.get('recaptcha_challenge_field'),
###                request.POST.get('recaptcha_response_field'),
###                settings.RECAPTCHA_PRIVATE_KEY,
###                request.META['REMOTE_ADDR'],)

###            # See if the user correctly entered CAPTCHA information
###            # and handle it accordingly
###            if response.is_valid:
###                captcha_response = "You are human!"

###                # Save the data
###                formSet.save()
###                # Redirect to another URL
###                return HttpResponseRedirect('/ant/ant/thanks/')

###            else:
###                captcha_response = 'Please type in the two words exactly as shown below'
###
###    else:
###        formSet =  ContactFormSet(managementFormData)             # An unbound form
###
###    return render_to_response(
###        'ant/contact.html',
###        {
###            'formSet': formSet,
###            'captcha_response': captcha_response,
###        },
###        context_instance=RequestContext(request)
###    )
###
###def thanks(request):
###    return render_to_response(
###        'ant/thanks.html',
###        {},
###        context_instance=RequestContext(request)
###    )

def ns2test(request):
    return render_to_response(
        'ant/workspace/ns2_interface.html',
        {},
        context_instance=RequestContext(request)
    )


# AJAX requests
def html_simulator(request, object_id=2):
    template_file = 'ant/special/simulator_%s.html' % (object_id,)
    return render_to_response(
        template_file,
        {},
        context_instance = RequestContext(request)
    )

def get_exercise_problem(request, exercise_id):
    '''
    Return the problem statement for an exercise; problem_id is the PK
    of the Exercise table.
    '''
    ep = get_object_or_404(Exercise, id=exercise_id)
    ep.problem = ep.problem.replace('_STATIC_URL_', settings.STATIC_URL)
    if settings.DEBUG:  # Ajax delay demo
        #import time
        #time.sleep(1)
        pass

    return HttpResponse(ep.problem)

@ensure_csrf_cookie
def get_exercise_workspace(request, exercise_id, object_id, problem_id=1):
    '''
    Return the problem solving workspace for the selected exercise.
    object_id is required to select the workspace javascript file.
    '''
    #print exercise_id, object_id, problem_id
    ew = get_object_or_404(Exercise, id=exercise_id)

    if settings.DEBUG:  # Ajax delay demo
        #import time
        #time.sleep(1)
        pass
    request.session['theory_id'] = object_id
    request.session.modified = True

    wtype = ew.workspace.wtype
    if wtype == 'Inline':
        workspace = get_inline_workspace(object_id, problem_id)
    else: # Either ns2 or ns3 interface
        template = None
        default_code = get_object_or_404(DefaultCode, exercise__id=exercise_id).code

        if wtype == 'ns3':
            template = 'ant/workspace/ns3_interface.html'
        else:   # By default ns2 workspace
            template = 'ant/workspace/ns2_interface.html'

        workspace = render_to_string(
            template,
            {
                #'MEDIA_URL': '/cse28/ant/v_media/',
                'object_id':    object_id,
                'problem_id':   problem_id,
                'default_code': default_code ,
            },
            request=request
            #context_instance=RequestContext(request)
        )
    return HttpResponse(workspace)


# An extremely simple, but very lengthy function
def get_inline_workspace(object_id, problem_id):
    entries = []
    object_id = int(object_id)
    problem_id = int(problem_id)
    #print object_id, problem_id

    template = 'ant/workspace/inline_workspace_%d.html' % (object_id,)
#    print template
    html = render_to_string(
        template,
        {
            'MEDIA_URL': '/cse28/ant/v_media/',
            'object_id': object_id,
            'problem_id': problem_id,
        },
        #context_instance=RequestContext(request)
    )
    return html

def get_exercise_answer(request, object_id=9, exercise_id=1):
    #if not request.is_ajax():
    #    return HttpResponse("You can't view this page!", status=400)

    s = get_object_or_404(Solution, exercise=exercise_id)

    mesgToDisplay = "<div class='centerAlign'> <input type='button' value='View Solution' "
    mesgToDisplay += "onclick='confirm(\"Are you sure you want to view the solution?\") ? window.open(\"/ant/ant/show_solution/%s/\", \"AntSolution\",\"width=800,height=600,resizable=yes,toolbar=no,linkbar=no,scrollbars=yes,location=0,directories=no,status=no,menubar=no,copyhistory=no\",false) : \"False\" ' />"
    mesgToDisplay += "</div>"
    mesgToDisplay = mesgToDisplay % (exercise_id,)
    return HttpResponse(mesgToDisplay)


def show_solution(request, object_id=9, exercise_id=1):
    s = get_object_or_404(Solution, exercise=exercise_id)
    s.image_url = s.image_url.replace('_STATIC_URL_', settings.STATIC_URL)
    return render_to_response(
        'ant/solution.html',
        {
            'solution_image':   s.image_url,
            'solution_text':    s.other,
        },
        context_instance=RequestContext(request),
    )

def comments(request, object_id=1):
    theory = get_object_or_404(Theory, pk=object_id)

    return render_to_response(
        'comments/list.html',
        {
            'theory':   theory,
        },
        context_instance = RequestContext(request)
    )


# (Rev #25: #3)
def verify_recaptcha(request):
    response = captcha.submit(
        request.GET.get('recaptcha_challenge_field'),
        request.GET.get('recaptcha_response_field'),
        settings.RECAPTCHA_PRIVATE_KEY,
        request.META['REMOTE_ADDR'],
    )

    # See if the user correctly entered CAPTCHA information
    # and handle it accordingly
    if response.is_valid:
        # OK
        return HttpResponse('Ok')
    else:
        return HttpResponse('***Error***')


# (Change #24 : #1)
def tinymce(request):
    return render_to_response(
        'ant/tinymce.html',
        {},
        context_instance=RequestContext(request)
    )

# Change #21: #4
def export2pdf(request):
    #print request.get_full_path(), request.session
    pass


# Submit a Celery task to execute ns2 code
# Returns UUID of the created task
def ns2test_submit(request):
    # (Rev #32: #1)
    #return exercises.ns2_submit(request)
    output = {}
    if request.method == 'POST':
        #print 'Submitting task ...'
        code = request.POST.get('ns2code')
        session_key = request.session.session_key
        #print 'Session key:', session_key
        try:
            new_task = tasks.ns2run.delay(code, session_key)
        ##print '<b>%d</b>' % (result.get(),)
            #print 'Simulation # :', new_task.task_id
            output['id'] = new_task.task_id
        except Exception, ex:
            output['error'] = 'Failed to submit simulation!\n%s' % ex
            #print ex
    else:
        output['error'] = 'Invalid attempt to access a resource!'

    return HttpResponse(json.dumps(output), content_type='application/json')


# (Rev #35: #2)
# Get trace file of the most recent simulation based on user's session ID
def get_trace_file(request):
    pass


# Rev#6: #4
def ns3(request):
    # (Rev #32: #2)
    return render_to_response(
        'ant/workspace/ns3_interface.html',
        {
            'defaultCode': '#include <iostream>'
        },
        context_instance=RequestContext(request)
    )


def ns3_submit(request):
    # (Rev #32: #1)
    #return exercises.ns3_submit(request)
    output = {}
    if request.method == 'POST':
        #print 'Sumitting task ...'
        code = request.POST.get('ns3code')
        session_key = request.session.session_key
        new_task = tasks.ns3run.delay(code, session_key)
        #print '<b>%d</b>' % (result.get(),)
        #print 'Simulation # :', new_task.task_id
        output['id'] = new_task.task_id
    else:
        output['error'] = 'Invalid attempt to access a resource!'

    return HttpResponse(json.dumps(output), content_type='application/json')


def url_test(request):
    pass


def ajax_test(request):
    e = get_list_or_404(Exercise, theory=9)
    return render_to_response(
        'test/jqry.html',
        {
            'exercise': e,
        },
        context_instance=RequestContext(request)
    )

def xhr_test(request):
    if request.is_ajax():
        message = "Hello, AJAX!"
    else:
        message = "Hello!"
    return HttpResponse(message)
