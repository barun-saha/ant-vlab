from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

     #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     # (Change #50)
     #(r'^ant/shoutbox/',        include('vlabs.shoutloud.urls')),
     
     # (Change #23: #1)
     #(r'^ant/ns2trace/',        include('vlabs.ns2trace.urls',)),
     #(r'^ant/ant/ns2trace/',    include('vlabs.ns2trace.urls',)),
     #(r'^ant/ant/ant/ns2trace/',    include('vlabs.ns2trace.urls',)),
     (r'^ns2trace/ns2trace/ns2trace/',    include('vlabs.ns2trace.urls',)),
     (r'^ant/ant/ns2trace/',    include('vlabs.ns2trace.urls',)),
     (r'^ant/ns2trace/',        include('vlabs.ns2trace.urls',)),

     # Development
     (r'^ant/ant/ant/',             include('vlabs.ant.urls')),
     (r'^ant/ant/',             include('vlabs.ant.urls')),
     # Production
     (r'^ant/',                 include('vlabs.ant.urls')),

     # Uncomment the next line to enable the admin:
     (r'^admin/',               include(admin.site.urls)),
)

