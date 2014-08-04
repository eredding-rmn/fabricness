# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: fluentd/td-agent

from common import *

__all__ = [
    'df',
    'hdparm'
]

@task
@parallel
def df():
    '''
    df -h, yo
    '''
    with settings(hide('everything'), warn_only=True):
        rslt = run('df -h')
        if rslt.succeeded:
            print("> {0}  ######################".format(env.host_string))
            print(rslt)
            return True
        else:
            return None

@task
@parallel
def hdparm(block_device, runs=50):
    '''
    run hdparm -t --direct <block_device>

    Arguments:
        block_device:string
        runs:int
    '''
    c_output = re.compile('Timing O_DIRECT (\w+) reads:\s+\w+\s+MB in\s+\S+ seconds = (\S+) MB/sec')
    test_rst = []
    with settings(
        hide('everything'),
        warn_only=True
            ):
        rslt = sudo('for x in $(seq 1 {}); do hdparm -tT --direct {}; done'.format(runs, block_device))
        for line in rslt.splitlines():
            stats = c_output.search(line)
            if stats:
                test, speed = stats.groups()
                test_rst.append({test: float(speed)})
                #print("{} {}".format(test, speed))
        test_sums = {}
        if test_rst:
            for run in test_rst:
                for r_type in run.iterkeys():
                    try:
                        test_sums[r_type] += run.get(r_type)
                    except KeyError:
                        test_sums[r_type] = run.get(r_type)
            print "=== {} HDPARM RESULTS for disk: {} ====".format(env.host_string, block_device)
            print "{:<10}    {:>10}".format('TEST', 'AVG')
            for r_type in test_sums.iterkeys():
                print "{:<10}    {:>10}".format(r_type, test_sums.get(r_type) / float(runs))

