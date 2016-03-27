from django.conf.urls import patterns
from django.conf.urls import *
from ant.models import *
from django.conf import settings

urlpatterns = patterns('ant.views',
    url(r'^$',                                 'index',                 name='index_page'),
    url(r'^(?P<object_id>\d+)/$',              'introduction',          name='introduction'),
    url(r'^(?P<object_id>\d+)/theory/$',       'theory',                name='theory'),
    url(r'^(?P<object_id>\d+)/procedure/$',    'procedure',             name='procedure'),
    url(r'^(?P<object_id>\d+)/simulation/$',   'simulation',            name='simulation'),
    url(r'^(?P<object_id>\d+)/self_evaluation/$',     'self_evaluation',      name='self_evaluation'),
    url(r'^(?P<object_id>\d+)/exercise/$',      'exercise',             name='exercise'),
    url(r'^(?P<object_id>\d+)/references/$',    'references',           name='references'),
    url(r'^about_us/$',                         'about_us',             name='about_us'),
    url(r'^license/$',                         'license',             name='license'),
##    url(r'^contact/$',                          'contact',         name='contact'),
##    url(r'^thanks/$',                           'thanks',         name='thanks'),
    url(r'^ns2_test/$',                         'ns2test',),
    url(r'^ns2_test_submit/$',                  'ns2test_submit',       name='ns2_submit',),
    # (Rev #35: #2)
    url(r'^get_trace_file/$',                   'get_trace_file',       name='get_trace_file',),
    # Rev #6: #3
    url(r'^ns3_interface/$',                    'ns3',                  name='ns3',),
    url(r'^ns3_submit/$',                       'ns3_submit',           name='ns3_submit',),
    # (Change #24 : #1)
    url(r'^tinymce/$',                          'tinymce',),
    # (Rev #25: #4)
    url(r'recaptchajaX/$',                      'verify_recaptcha'),
)

###urlpatterns += patterns('',
###    url(r'^comments/', include('django.contrib.comments.urls'),         name='comments'),
###    url(r'^(?P<object_id>\d+)/theory/load_comments/$', 'vlabs.ant.views.comments',  name='theory_comments'),
###)

# Ajax based request URLs
urlpatterns += patterns('ant.views',
    url(r'^load_exercise/(?P<exercise_id>\d+)/$',    'get_exercise_problem',     name='get_problem',),
    url(r'^load_workspace/(?P<exercise_id>\d+)/(?P<object_id>\d+)/(?P<problem_id>\d+)/$',   'get_exercise_workspace', name='get_workspace',),
    #url(r'^wireit/$',                               'wireit',),
    url(r'^answer/(?P<object_id>\d+)/(?P<exercise_id>\d+)/$',           'get_exercise_answer', name='get_answer',),
    url(r'^show_solution/(?P<exercise_id>\d+)/$',    'show_solution',           name='get_solution',),
    # HTML based simulator
    url(r'^(?P<object_id>\d+)/html_sim/$',          'html_simulator',           name='html_simulator',),
    # Change #21: #4
    url(r'^export2pdf/$',                           'export2pdf'),
)

# Python RQ
urlpatterns += patterns('ant.tasks',
    url(r'^job/result/(?P<uuid>[a-z0-9\-]+)/$',                  'job_result', name='job_result',),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^v_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^xhr_test$',  'ant.views.xhr_test'),
        url(r'^ajax/$',     'ant.views.ajax_test'),
        url(r'^url_test/$',     'ant.views.url_test'),
    )
