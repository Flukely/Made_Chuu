# filepath: /c:/Users/milk/OneDrive - Naresuan University/เดสก์ท็อป/MadeChuu/MadeChuu/index/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MadeChuu.settings')

application = get_wsgi_application()