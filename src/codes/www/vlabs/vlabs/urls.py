from django.conf.urls import include, url, patterns

# Serve URLs of both the apps from / (root) --
# as of now at least
urlpatterns = patterns('',
     (r'^', include('ant.urls')),
     (r'^', include('ns2trace.urls')),
)
