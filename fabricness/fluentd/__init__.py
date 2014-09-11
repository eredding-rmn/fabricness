# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: fluentd/td-agent

from common import *
from lib.stfutask import StfuTask

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
def monitor_api(port=24220):
    '''
    curl call the monitoring API locally
    '''
    if util.check_for_binary('curl'):
        with settings(hide('everything'), warn_only=True):
            rslt = sudo('curl -s http://localhost:{0}/api/plugins.json'.format(port))
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
    if service.restart("td-agent"):
        puts('> {0} :: td-agent restarted'.format(env.host_string))
        return True
    else:
        warn('> {0} :: td-agent did not restart'.format(env.host_string))
        return False


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
        return True
    else:
        return False


@task(task_class=StfuTask)
@parallel(pool_size=7)
def cond_restart():
    '''
    Only restart if td-agent is installed and running
    '''
    with settings( hide('everything'), show('stdout'),warn_only=True,skip_bad_hosts=True ):
        if is_installed() and util.pgrep(binary_name='td-agent', user='td-agent'):
            if not re.search('fld-agg', env.host_string):
                return restart()
