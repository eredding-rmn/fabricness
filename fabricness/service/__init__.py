# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: SERVICE

from common import *

__all__ = [
    'restart',
    'stop',
    'start',
    'status'
]

@task
@parallel(pool_size=7)
def restart(service):
    '''
    ** run /etc/init.d/<service> restart

    Args:
        service:string
    '''
    try:
        command = "/etc/init.d/{0} restart".format(service)
        with settings(warn_only=True):
            rslt = util.sudo_command("{}".format(command))
            if rslt.succeeded:
                return True
            else:
                return False
    except TypeError:
        warn('invalid parameter!')


@task
@parallel(pool_size=7)
def stop(service):
    '''
    ** run /etc/init.d/<service> stop

    Args:
        service:string
    '''
    try:
        command = "/etc/init.d/{0} stop".format(service)
        with settings(warn_only=True):
            rslt = util.sudo_command("{}".format(command))
            if rslt.succeeded:
                return True
            else:
                return False
    except TypeError:
        warn('invalid parameter!')


@task
@parallel(pool_size=7)
def start(service):
    '''
    ** run /etc/init.d/<service> start

    Args:
        service:string
    '''
    try:
        command = "/etc/init.d/{0} start".format(service)
        with settings(warn_only=True):
            rslt = util.sudo_command("{}".format(command))
            if rslt.succeeded:
                return True
            else:
                return False
    except TypeError:
        warn('invalid parameter!')


@task
@parallel(pool_size=7)
def status(service):
    '''
    ** run /etc/init.d/<service> status

    Args:
        service:string
    '''
    try:
        command = "/etc/init.d/{0} status".format(service)
        with settings(warn_only=True):
            rslt = util.sudo_command("{}".format(command))
            if rslt.succeeded:
                return True
            else:
                return False
    except TypeError:
        warn('invalid parameter!')