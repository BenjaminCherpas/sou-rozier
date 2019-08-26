#!/home/apidev/.python/python2.7/bin/python

import os
import sys


_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# setup the virtualenv
venv = os.path.abspath(_PROJECT_DIR+'/env/bin/activate_this.py')
execfile(venv, dict(__file__=venv))

sys.path.insert(0, _PROJECT_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = "pierres_folles.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")