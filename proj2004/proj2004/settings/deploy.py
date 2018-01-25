import yaml

from . import *

CONF_DIR = os.path.join(os.path.dirname(BASE_DIR), 'conf')
with open(os.path.join(CONF_DIR, 'settings.yml')) as config_file:
    config = yaml.load(config_file)

DEBUG = False
SECRET_KEY = config['secret_key']
ALLOWED_HOSTS = config['allowed_hosts']
DATABASES = {
    'default': config['db'],
}
WWW_ROOT = '/var/www'
STATIC_ROOT = os.path.join(WWW_ROOT, 'static')
MEDIA_ROOT = os.path.join(WWW_ROOT, 'media')
