# -*- coding: UTF-8 -*-
################################################################
# cpu.py
################################################################
#  Run CPU-based tests!
################
from common import *


__all__ = [
    'sysbench_thread'
]

SYSBENCH_CMD='sysbench --num-threads=%{threads} --test=threads --thread-yields=%{yields} --thread-locks=%{locks} run'


@task
@parallel
def sysbench_thread(iterations=50,threads=64,yields=100,locks=2):
    '''
    run sysbench CPU test command 50 times (default): sysbench --num-threads=%{threads} --test=threads --thread-yields=%{yields} --thread-locks=%{locks} run
    Args:
        iterations:int
        threads:int
        yields:int
        locks:int

    '''
    arglist={
        'threads': threads,
        'yields': yields,
        'locks': locks
    }
    with settings(warn_only=True):
        if util.check_for_binary('sysbench'):
            try:
                for x in xrange(0, iterations):
                    util.sudo_command(SYSBENCH_CMD.format(arglist))
            except TypeError:
                warn('invalid input!')
                sys.exit(1)
        else:
            warn('sysbench not found! quitting..')
