# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity;
#
#  LIBRARY FUNCTIONS: things that use libraries to get things!
#  Note: Don't add tasks here; just library functions.


from common import *

def get_ec2_hosts(region, profile, filters):
    '''
    acky call to list hosts and set the env.hosts list in python
    '''
    from acky.aws import AWS
    try:
        aws_conn = AWS(region, profile)
        hosts_list=aws_conn.ec2.Instances.get(filters=filters)
        for host in hosts_list:
            hn = get_tag(host, 'Name')
            if not hn:
                hn = host.get('PublicIpAddress')
            env.hosts.append(hn)
    except Exception as e:
        warn('error setting hosts: {0}'.format(e.message))


def get_tag(tags, tagname):
    '''
    get a tag by name, from either a tags data structure or a pile of stuff with a Tags key
    '''
    try:
        ltags = tags.get('Tags')
    except:
        ltags = None
    if not ltags:
        ltags = tags
    for tag in ltags:
        if tag.get('Key') == tagname:
            return tag.get('Value')