# import os
# import sys


# sys.path.insert(0, os.path.dirname(__file__))


# def application(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works!\n'
#     version = 'Python %s\n' % sys.version.split()[0]
#     response = '\n'.join([message, version])
#     return [response.encode()]



import sys, os
INTERP = "/home/duinqvdw/virtualenv/backend/3.9/bin/python"
#INTERP is present twice so that the new Python interpreter knows the actual executable path
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

os.environ['DJANGO_SETTINGS_MODULE'] = "coresite.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
