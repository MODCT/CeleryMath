# 并行工作进程数 核心数*2+1个
workers = 3
# 指定每个工作者的线程数
threads = 2
# 监听内网端口
bind = '127.0.0.1:8000'
# 设置守护进程
daemon = 'false'
# 工作模式协程
worker_class = 'gevent'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = '/var/run/gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = '/var/log/gunicorn_access.log'
errorlog = '/var/log/gunicorn_error.log'
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = 'debug'

capture_output = True
