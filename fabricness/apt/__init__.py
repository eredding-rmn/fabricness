# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: apt

from common import *


__all__ = [
    'clear_cache',
    'update',
    'rm_lists',
    'full_refresh'
]


@task
@parallel
def clear_cache():
    '''
    run apt-get clean

    Args:

    '''
    command = "apt-get clean"
    with settings(warn_only=True):
        rslt = util.sudo_command("{}".format(command))
        if rslt.succeeded:
            return True
        else:
            return False


@task
@parallel
def update():
    '''
    run apt-get update

    Args:

    '''
    command = "apt-get update"
    with settings(warn_only=True):
        rslt = util.sudo_command("{}".format(command))
        if rslt.succeeded:
            return True
        else:
            return False


@task
@parallel
def rm_lists(listname=None):
    '''
    removes all or a single file from /var/lib/apt/lists/

    Args:

    '''
    if listname:
        command = "rm -rf /var/lib/apt/lists/{0}".format(listname)
    else:
        command = "rm -rf /var/lib/apt/lists/"
    with settings(warn_only=True):
        rslt = util.sudo_command("{}".format(command))
        if rslt.succeeded:
            return True
        else:
            return False

@task
@parallel
def full_refresh():
    '''
    destructively refreshes apt by purging known lists and then running apt-get update
    '''
    with settings(warn_only=True):
        execute(rm_lists)
        execute(clear_cache)
        execute(update)
