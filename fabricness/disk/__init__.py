# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: disk

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


@task
@parallel
def cuddler(volume):
    '''
    WAARM YER DISKS YA HEARD.  Need to set host, and hand it a block device path: i.e. /dev/xvdca
    Args:
        volume
    Returns:
        bool
    '''
    # sudo kill -USR1 $(pgrep '^dd') shows progress... how do we set up a timer to barf that out periodically? not with fabric...
    with settings(warn_only=True):
        rslt = sudo('dd if=/dev/zero of={0} bs=1M'.format(volume))
        if rslt.succeeded:
            puts("yer disk {} has been spooned on a bear-skin rug in front of a fireplace... it's ready for your use".format(volume))
            return True
        else:
            return False


@task
@parallel
def mk_ext4(block_device="/dev/yourmom"):
    '''
    make a block device ext4; use with extreme caution
    ex: fab -H <hostname> mk_ext4:'/dev/md999'

    Args:
        block_device
    Returns:
        bool
    '''
    mkfs = sudo("time mkfs.ext4 {}".format(block_device))
    if mkfs.succeeded:
        return True
    else:
        abort('mkfs failed')
        return False


@task
def set_readahead_for_device(device):
    '''
    configure readahead for block device
      executes command and appends it to rc.local

    Args:
        device:string

    Returns:
        bool
    '''
    setcmd = sudo(
        'echo "blockdev --setra 2048 {}" | tee -a /etc/rc.local | bash'.format(
            device
        )
    )
    if setcmd.succeeded:
        return True
    else:
        abort('set readahead failed')
        return False
