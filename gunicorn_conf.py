from multiprocessing import cpu_count



# Socket Path

bind = 'unix:/home/rob/csvExport/gunicorn.sock'



# Worker Options

workers = cpu_count() + 1

worker_class = 'uvicorn.workers.UvicornWorker'



# Logging Options

loglevel = 'debug'

accesslog = '/home/rob/csvExport/access_log'

errorlog =  '/home/rob/csvExport/error_log'
