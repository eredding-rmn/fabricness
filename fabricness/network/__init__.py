# -*- coding: UTF-8 -*-
################################################################

from fabric.colors import *
from fabric.api import *

number_format='M'

"""
Example of use:
fab network.run_test:perf_port=24224,perf_server=firsthost,perf_client=secondhost
"""

__all__ = [
    'run_test'
]

@task
def run_test(perf_port, perf_client, perf_server):
    '''
     set the "server" role in the iperf test

    Args:
        perf_server:string
    '''
    with settings(clean_revert=True):
        env.perf_port = perf_port
        env.perf_server = perf_server
        env.perf_client = perf_client
        execute(start_server)
        execute(start_client)
        execute(stop_iperf_server, hosts=[env.perf_server])


def perf_port(perf_port):
    '''
     set the "port" flag in iperf

    Args:
        port:string
    '''
    with settings(clean_revert=True):
        env.perf_port = perf_port


def start_server():
    '''
     set the "server" role in the iperf test

    Args:
        perf_server:string
    '''

    iperfserver = execute(start_iperf_server, hosts=[env.perf_server])
    if False not in iperfserver.values():
        puts("server started: {0}".format(iperfserver.values()))


@task
@parallel
def start_client():
    '''
     set the "server" role in the iperf test

    Args:
        perf_client:string
    '''
    iperfclient = execute(start_iperf_client, hosts=[env.perf_client])


@task
@parallel
def start_iperf_server():
    require('perf_port')
    iperf_flag_port = '--port {0}'.format(env.perf_port)
    iperf_format = '--format {0}'.format(number_format)
    sudo('iperf -D --server {0} -o {1}.iperf.log {2} 2>&1; sleep 2'.format(iperf_format, env.host_string, iperf_flag_port))


@task
def stop_iperf_server():
    '''
    stop iperf server
    '''
    sudo('pkill -9 iperf')


@task
@parallel
def start_iperf_client():
    '''
    start iperf client
    '''
    require('perf_server')
    require('perf_port')
    iperf_flags_client = '--client {0}'.format(env.perf_server)
    iperf_flag_port = '--port {0}'.format(env.perf_port)
    iperf_format = '--format {0}'.format(number_format)
    sudo('iperf {0}  {1}  {2} -t 60 -i 10'.format(iperf_format, iperf_flag_port, iperf_flags_client))