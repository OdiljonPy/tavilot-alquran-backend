project_name = 'tavilot-alquran-backend'

wsgi_app = "config.wsgi:application"
loglevel = 'debug'
workers = 1
bind = '0.0.0.0:8001'
reload = False
accesslog = errorlog = f'/var/log/gunicorn/{project_name}-dev.log'
capture_output = True
pidfile = f'/var/run/gunicorn/{project_name}-dev.pid'
# daemon = True
