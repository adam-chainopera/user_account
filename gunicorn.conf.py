# gunicorn config
# import multiprocessing

# server socket
bind = "0.0.0.0:8000"
backlog = 2048

# worker process
import multiprocessing
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# restart
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# log
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# process name
proc_name = "wallet-api"