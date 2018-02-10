import yaml

from .common import *

DEBUG = False
WWW_ROOT = '/var/www'

CONF_DIR = os.path.join(BASE_DIR, 'conf')
try:
    with open(os.path.join(CONF_DIR, 'settings.yml')) as config_file:
        config = yaml.load(config_file)
    globals().update(config)
    del config, config_file
except FileNotFoundError:
    pass
del yaml

if 'STATIC_ROOT' not in globals():
    STATIC_ROOT = os.path.join(WWW_ROOT, 'static')
if 'MEDIA_ROOT' not in globals():
    MEDIA_ROOT = os.path.join(WWW_ROOT, 'media')
