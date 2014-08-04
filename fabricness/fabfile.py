# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity
#
# Note: Never set __all__ here; this is top-level scope
#
from common import *



@task
def profile(aws_profile):
    '''
    Sets global variable for an aws config profile in ~/.aws/config.  set when leveraging aws-cli utility calls prefixed with AWS in help

    Args:
        aws_profile:string
    '''
    with settings(clean_revert=True):
        env.aws_profile = aws_profile


@task
def region(aws_region):
    '''
    Sets global variable for an aws region.  set when leveraging aws-cli utility calls prefixed with AWS in help

    Args:
        aws_region:string
    '''
    with settings(clean_revert=True):
        env.aws_region = aws_region


@task
def set_hosts_by_ident(ident):
    '''
    AWS: set the hosts variable via aws cli command that filters on the name tag; ident is the unique identifier in the name tag.

    Requires: region, profile

    Args:
        ident:string
    '''
    require('aws_profile')
    require('aws_region')

    lib.get_ec2_hosts(region=env.aws_region,profile=env.aws_profile,filters={'tag:Name': '*{0}*'.format(ident), 'instance-state-name': 'running'})
    print("{0} {1}".format(green('set hosts: '),green(env.hosts)))


@task
def set_all_hosts():
    '''
    AWS: set the hosts variable via aws cli command that filters on the name tag; ident is the unique identifier in the name tag.

    Requires: region, profile

    Args:
        ident:string
    '''
    require('aws_profile')
    require('aws_region')

    lib.get_ec2_hosts(region=env.aws_region,profile=env.aws_profile,filters={'instance-state-name':'running'})
    print("{0} {1}".format(green('set hosts: '),green(env.hosts)))