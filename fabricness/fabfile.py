# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity




from common import *
import util

@task
def environment(aws_environment):
    '''
    ** Sets environments named in ~/.aws/config file. Required by all actions
        See: https://wiki.whalesharkmedia.com/display/GEO/Situ#Situ-Creden
    Args:
        aws_environment:string
    '''
    with settings(clean_revert=True):
        env.aws_environment = aws_environment