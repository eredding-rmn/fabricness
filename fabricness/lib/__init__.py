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


def get_ec2_hosts(region, profile, filters, avpc=None):
    '''
    acky call to list hosts and set the env.hosts list in python
    '''
    raw_hosts_list = get_hostlist(region, profile, filters, avpc)
    if not raw_hosts_list:
        abort('no hosts found!')
    host_map = filter_hosts_by_ec2_type(raw_hosts_list)

    if avpc:
        env.hosts = host_map.get(avpc).get('hosts')
        if not env.hosts:
            abort('specified vpc ({0}) was not found'.format(avpc))
        if host_map.get(avpc).get('gateway'):
            env.gateway = host_map.get(avpc).get('gateway')
    else:
        env.hosts = host_map.get('classic').get('hosts')
        if not env.hosts:
            for vpc in host_map.iterkeys():
                env.hosts = host_map.get(vpc).get('hosts')
                if env.hosts:
                    if host_map.get(vpc).get('gateway'):
                        env.gateway = host_map.get(vpc).get('gateway')
                    break
        else:
            if host_map.get('classic').get('gateway'):
                env.gateway = host_map.get('classic').get('gateway')
    return True


def get_aws_connection(region, profile):
    from acky.aws import AWS
    try:
        aws_conn = AWS(region, profile)
    except Exception as e:
        abort('connection error!  message: {0}'.format(e))
        return False
    return aws_conn


def get_hostlist(region, profile, filters, avpc=None):
    aws_conn = get_aws_connection(region, profile)
    try:
        return aws_conn.ec2.Instances.get(filters=filters)
    except Exception as e:
        abort('get instance error: {0}'.format(e))
        return False


def set_host_alias_list(host, alias):
    env.host_aliases[host] = alias


def filter_hosts_by_ec2_type(raw_hosts_list):
    ec2_host_mapping = {
        'classic': {
            'hosts': [],
            'gateway': None
        }
    }
    for hst in raw_hosts_list:
        vpcid = hst.get('VpcId')
        hn = get_tag(hst, 'Name')
        ip = hst.get('PrivateIpAddress')
        gwfound = re.search(env.gateway_host_ident, hn)
        if not hn:
            hn = ip
        if vpcid is None:
            ec2_host_mapping['classic']['hosts'].append(hn)
            if gwfound:
                ec2_host_mapping['classic'].update({'gateway': hn})
        else:
            # if we we don't see the vpc, we stub out the corpse
            if not ec2_host_mapping.get(vpcid):
                ec2_host_mapping[vpcid] = {'hosts': [], 'gateway': None}
            ec2_host_mapping[vpcid]['hosts'].append(hn)
            if gwfound:
                ec2_host_mapping[vpc].update({'gateway': hn})
        set_host_alias_list(hn, ip)
    return ec2_host_mapping


def get_tag(tags, tagname):
    '''
    get a tag by name, from either a tags data structure or
      a pile of stuff with a Tags key
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
