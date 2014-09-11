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
        return True


@task
def region(aws_region):
    '''
    Sets global variable for an aws region.  set when leveraging aws-cli utility calls prefixed with AWS in help

    Args:
        aws_region:string
    '''
    with settings(clean_revert=True):
        env.aws_region = aws_region
        return True


@task
def set_hosts_by_ident(ident,vpc_id=None):
    '''
    AWS: set the hosts variable via aws cli command that filters on the name tag; ident is the unique identifier in the name tag.

    Requires: region, profile

    Args:
        ident:string
        vpc_id:string (none by default)
    '''
    require('aws_profile')
    require('aws_region')
    if not ident:
        abort("an identifier is required!")
    try:
        lib.get_ec2_hosts(region=env.aws_region,profile=env.aws_profile,filters={'tag:Name': '*{0}*'.format(ident), 'instance-state-name': 'running'},avpc=vpc_id)
    except Exception as e:
        abort("failure during host list generation!  message: {0}".format(e))
    if env.hosts:
        print("{0}".format(green('set hosts: ')))
        for host in env.hosts:
            print ("    {0}".format(green(host)))
        return True
    else:
        abort("!!!! {0} !!!!".format(red('NO HOSTS FOUND')))
        return False


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
    if env.hosts:
        puts("{0}".format(green('set hosts: ')))
        for host in env.hosts:
            puts(":: {0}".format(green(host)))
        return True
    else:
        warn("!!!! {0} !!!!".format(red('NO HOSTS FOUND')))
        return False

@task
def set_hosts_by_ec2_type(vpc='classic'):
    '''
    AWS: set the hosts variable via aws API; filters on vpc-id value.
        Valid inputs are either 'classic' (default) or a legitimate VpcId value.

    Requires: region, profile

    Args:
        vpc:string
    '''
    require('aws_profile')
    require('aws_region')
    MATCHVPC=re.compile('vpc-\S{8}')
    if vpc == 'classic':
        myfilters = {'instance-state-name': 'running'}
    if MATCHVPC.match(vpc):
        myfilters = {'vpc-id': vpc, 'instance-state-name': 'running'}
    lib.get_ec2_hosts(region=env.aws_region,profile=env.aws_profile,filters=myfilters, avpc=vpc)

    if env.hosts:
        print("{0}".format(green('set hosts: ')))
        for host in env.hosts:
            print ("    {0}".format(green(host)))
        return True
    else:
        print("!!!! {0} !!!!".format(red('NO HOSTS FOUND')))
        return False


@task
def show_hosts():
    print("####++++++>>>> host list:  ")
    print("host list:  ")
    print(env.hosts)
    print("<<<<++++++####")
    return True