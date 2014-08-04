# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case, SENSU

from common import *

__all__ = [
    'restart_client',
    'stop_client',
    'start_client',
    'status_client',
    'client_version',
    'server_version',
    'puppet_sensu_server',
    'restart_server',
    'restart_api',
    'restart_dashboard'
]


@task
@parallel(pool_size=7)
def restart_client():
    '''
    restart sensu client
    '''
    service.restart("sensu-client")

@task
@parallel(pool_size=7)
def status_client():
    '''
    restart sensu client
    '''
    service.status("sensu-client")


@task
@parallel(pool_size=7)
def stop_client():
    '''
    stop sensu client
    '''
    service.stop("sensu-client")



@task
@parallel(pool_size=7)
def start_client(debug=False):
    '''
    start sensu client
    '''
    service.start("sensu-client")



@task
@parallel(pool_size=7)
def client_version():
    '''
    return the sensu client version
    '''
    command = "/opt/sensu/embedded/bin/ruby /opt/sensu/bin/sensu-client --version"
    with settings(warn_only=True):
        rslt = util.sudo_command(command)
        if rslt.succeeded:
            return True
        else:
            return None


@task
@parallel(pool_size=11)
def server_version(debug=False):
    '''
    return the sensu server version
    '''
    command = "/opt/sensu/embedded/bin/ruby /opt/sensu/bin/sensu-server --version"
    with settings(warn_only=True):
        if debug:
            command = command + ' -v'
        rslt = util.sudo_command("{}".format(command))
        if rslt.succeeded:
            return True
        else:
            return None



@task
@parallel(pool_size=11)
def puppet_sensu_server(debug=False):
    '''
    run puppet, by specifiying the tag: profile_all::sensu::server
    '''
    puppet.by_tag('profile_all::sensu::server', debug)



@task
@parallel(pool_size=11)
def restart_server():
    '''
    restart sensu server service
    '''
    service.restart('sensu-server')


@task
@parallel(pool_size=11)
def restart_api(debug=False):
    '''
    restart sensu API service
    '''
    service.restart('sensu-api')


@task
@parallel(pool_size=11)
def restart_dashboard(debug=False):
    '''
    restart sensu dashboard service
    '''
    service.restart('sensu-dashboard')