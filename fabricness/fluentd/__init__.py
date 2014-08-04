# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: fluentd/td-agent

from common import *

__all__ = [
    'check_status',
    'monitor_api',
    'procs',
    'status',
    'start',
    'stop',
    'restart',
    'cond_restart'
]


@task
@parallel(pool_size=7)
def monitor_api():
    '''
    curl call the monitoring API locally
    '''
    if util.check_for_binary('curl'):
        with settings(hide('everything'), warn_only=True):
            rslt = sudo('curl -s http://localhost:24220/api/plugins.json')
            if rslt.succeeded:
                import json
                jsrslt = json.loads(rslt)
                print(green("> {0} ##############".format(env.host_string)))
                print(json.dumps(jsrslt))
                return True
            else:
                return False


@task
@parallel(pool_size=7)
def procs():
    '''
    td-agent service status
    '''
    with settings(hide('everything'), warn_only=True):
        rslt = util.pgrep(binary_name='td-agent',user='td-agent')
        if rslt.succeeded:
            print "> {0}:   {1}".format(env.host_string, rslt)
            return True
        else:
            return False

@task
@parallel(pool_size=7)
def status():
    '''
    td-agent service status
    '''
    service.status("td-agent")


@task
@parallel(pool_size=7)
def restart():
    '''
    restart td-agent
    '''
    service.restart("td-agent")


@task
@parallel(pool_size=7)
def stop():
    '''
    stop td-agent
    '''
    service.stop("td-agent")


@task
@parallel(pool_size=7)
def start():
    '''
    start td-agent
    '''
    service.start("td-agent")


@task
@parallel(pool_size=7)
def is_installed():
    '''
    check if td-agent is installed
    '''
    if util.dpkg_grep('td-agent'):
        if service.td-agent:
            return True
        else:
            return False

@task
@parallel(pool_size=7)
def cond_restart():
    if is_installed:
        return restart()