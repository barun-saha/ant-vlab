from django.conf.urls import include, url, patterns
from django.conf import settings
reverse_proxy_pattern = r'^%s' % (settings.REVERSE_PROXY_PREFIX,)
# Serve URLs of both the apps from / (root) --
# as of now at least
urlpatterns = patterns('',
     (reverse_proxy_pattern, include('ant.urls')),
     (reverse_proxy_pattern, include('ns2trace.urls')),
     (r'^', include('ant.urls')),
     (r'^', include('ns2trace.urls')),
)
