import yaml

from . import *

DEBUG = False
WWW_ROOT = '/var/www'
STATIC_ROOT = os.path.join(WWW_ROOT, 'static')
MEDIA_ROOT = os.path.join(WWW_ROOT, 'media')

CONF_DIR = os.path.join(BASE_DIR, 'conf')
try:
    with open(os.path.join(CONF_DIR, 'settings.yml')) as config_file:
        config = yaml.load(config_file)
    globals().update(config)
    del config, config_file
except FileNotFoundError:
    pass
del yaml
