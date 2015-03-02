import os
import sys

sys.path.append('/home/barun/codes/www')
sys.path.append('/home/barun/codes/www/vlabs')
os.environ['DJANGO_SETTINGS_MODULE'] = 'vlabs.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

