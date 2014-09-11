# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: fluentd/td-agent

from common import *

__all__ = [
    'stop_device',
    'make_raid',
]

@task
@parallel
def stop_device(raid_device):
    '''
    stop  a raid device
    Args:
        raid_device
    Returns:
        bool
    '''
    stopraid = sudo("mdadm --stop {} ".format(raid_device))
    if stopraid.succeeded:
        return True
    else:
        abort('mdadm stop failed')
        return False


@task
@parallel
def make_raid(raid_level, raid_device="/dev/md11", block_devs=None, raid_name=None):
    '''
    make raid device by specifying the level, raid block device, devices to raid, and the name of the array
    ex: fab -H <host>  disk.mdadm.make_raid:raid_level=0,block_devs="/dev/xvdca /dev/xvdcb /dev/xvdcc /dev/xvdcd /dev/xvdce /dev/xvdcf /dev/xvdcg /dev/xvdch",raid_device="/dev/md999",

    Args:
        raid_level:string
        block_devs:string
        raid_device:string
        raid_name:string
    Returns:
        bool
    '''
    if isinstance(block_devs, list):
        num_disks = len(block_devs)
        block_devs_str = " ".join(block_devs)
    else:
        if re.search(',', block_devs):
            block_dev_list = block_devs.split(',')
            num_disks = len(block_dev_list)
            block_devs_str = " ".join(block_dev_list)
        else:
            num_disks = len(block_devs.split())
        block_devs_str = block_devs
    if not raid_name:
        raid_name = 'raid_device'
    mkraid_command = (
        "echo 'yes' | "
        " mdadm --create --verbose {raid_device} "
        " --level={raid_level} "
        " --chunk=1024"
        " --name={raid_name}"
        " --raid-devices={num_disks} {block_devs}".format(
            raid_device=raid_device,
            raid_level=raid_level,
            raid_name=raid_name,
            num_disks=num_disks,
            block_devs=block_devs_str
        )
    )
    create_cmd = sudo(mkraid_command)
    if create_cmd.succeeded:
        sudo('cat /proc/mdstat')
        return True
    else:
        abort(
            'Failure creating raid device on host: {0}'.format(
                env.host_string
            )
        )
        return False
