"""
WSGI config for main_aas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_aas.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root='/main_aas-20220128T092040Z-001/main_aas/static')
application.add_files('/main_aas-20220128T092040Z-001/main_aas/static', prefix='more-files/')
