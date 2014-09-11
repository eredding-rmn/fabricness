# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: ebs

from common import *

__all__ = [
    'create_volume',
    'attach'
]

@task(task_class=AwsTask)
def create_volume(size, az):
    '''
    creates an ebs volume
    '''
    pass

@task(task_class=AwsTask)
#@aws_connection
def attach(volume_id):
    '''
    attach an ebs volume to current env.host_string

    if env.host_aliases[env.host_string].id
        attach the thing
    '''
    pass
