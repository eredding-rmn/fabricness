# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: PUPPET

from common import *


__all__ = [
    'by_tag',
    'noop',
    'agent'
]

## Puppet Run -- By tag
@task
@parallel
def by_tag(tags, debug=False):
    '''
    run puppet agent and specify a tag

    Args:
        tags:string
    '''
    try:
        command = "puppet agent -t --tags {0} --configtimeout 600".format(tags)
        with settings(warn_only=True):
            if debug:
                command = command + ' -v'
            rslt = util.sudo_command("{}".format(command))
            if rslt.succeeded:
                return True
            else:
                return False
    except TypeError:
        warn('invalid parameter!')


## Puppet Run -- NOOP
@task
@parallel
def noop(debug=False):
    '''
    run puppet agent in noop mode
    '''
    command = "puppet agent -t --noop --configtimeout 600"
    with settings(warn_only=True):
        if debug:
            command = command + ' -v'
        rslt = util.sudo_command("{}".format(command))
        if rslt.succeeded:
            return True
        else:
            return None


## Puppet Run -- All Classes
@task
@parallel
def agent(debug=False):
    '''
    run puppet agent (yeah - the whole thing)
    '''
    command = "puppet agent -t --configtimeout 600"
    with settings(warn_only=True):
        if debug:
            command = command + ' -v'
        rslt = util.sudo_command("{}".format(command))
        if rslt.succeeded:
            return True
        else:
            return None

@task
def puppetmaster_update():
    '''
        git pull repo and restart apache
    '''
    pass