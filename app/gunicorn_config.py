import multiprocessing

bind = '0.0.0.0:80'
workers = 4
#loglevel = 'debug'
errorlog = 'runtime_log.log'
syslog = False

# The Access log file to write to. [None]
accesslog ='gunicorn.access.log'

# The Access log format . [%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"]
access_log_format ='"%(h)s\t%(l)s\t%(u)s\t%(t)s\t"%(r)s"\t%(s)s\t%(b)s\t"%(f)s"\t"%(a)s"'