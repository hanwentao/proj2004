from .common import *

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}
