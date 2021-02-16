import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'reid.settings'
django.setup()
from retrieval.models import Object
