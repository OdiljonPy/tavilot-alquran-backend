"""Gunicorn *production* config file (suppose > prod.py)"""

"""Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME"""
project_name = 'tavilot-alquran-backend'
wsgi_app = "config.wsgi:application"
"""The granularity of Error log outputs"""
loglevel = "debug"
"""The number of worker processes for handling requests"""
workers = 2
"""The socket to bind"""
bind = "0.0.0.0:5001"
"""Restart workers when code changes (development only!)"""
reload = False
"""Write access and error info to /var/log"""
accesslog = errorlog = f"/var/log/gunicorn/{project_name}-prod.log"
"""Redirect stdout/stderr to log file"""
capture_output = True
"""PID file so you can easily fetch process ID"""
pidfile = f"/var/run/gunicorn/{project_name}-prod.pid"
"""Daemonize the Gunicorn process (detach & enter background)"""
# daemon = True

"""With the dev.py file above, run this"""
# gunicorn -c config/gunicorn/prod.py
