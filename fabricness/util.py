# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity


from common import *
@task
@parallel
def get_processorcount():
    rslt = sudo_command("facter processorcount")
    if rslt.succeeded:
        return int(rslt)
    else:
        return None


@task
@parallel
def get_physicalprocessorcount():
    rslt = sudo_command("facter physicalprocessorcount")
    if rslt.succeeded:
        return int(rslt)
    else:
        return None


@task
@parallel
def get_osfamily():
    rslt = run("facter osfamily")
    if rslt.succeeded:
        return "{}".format(rslt)
    else:
        return None


@parallel
def resolve_installer():
    osfamily = get_osfamily()
    with settings(clean_revert=True):
        if osfamily == "Debian":
            env.INSTALLER = "DEBIAN_FRONTEND=noninteractive apt-get -y"
        elif osfamily == "RedHat":
            env.INSTALLER = "yum -y"
        else:
            abort("The os_family fact didn't resolve to something we're aware of.  Aborting")
            exit(1)


@task
@parallel
def install_package(package):
    with settings(clean_revert=True):
        resolve_installer()
        require('INSTALLER')
        rslt = sudo_command("{} install {}".format(env.INSTALLER, package))
        if rslt.succeeded:
            return True
        else:
            return None


@task
@parallel
def command(command):
    '''
    run an arbitrary command; intended for use from within fabric because it will bust up cli arguments into a list
    '''
    with settings(warn_only=True):
        return run("%s" % command)


@task
@parallel
def sudo_command(command):
    '''
    run an arbitrary sudo command; intended for use from within fabric because it will bust up cli arguments into a list
    '''
    with settings(warn_only=True):
        return sudo(command)


@parallel
def check_for_binary(binary_name):
    with hide('everything'):
        we_good = run('which {}'.format(binary_name))
        if we_good.succeeded:
            return True
        else:
            return False

@task
@parallel
def volume_cuddler(volume):
    '''
    WAARM YER DISKS YA HEARD.  Need to set host, and hand it a block device path: i.e. /dev/xvdca
    Args:
        volume
    Returns:
        bool
    '''
    # sudo kill -USR1 $(pgrep '^dd') shows progress... how do we set up a timer to barf that out periodically?
    #require('environment')
    with settings(warn_only=True):
        rslt = sudo('dd if=/dev/zero of={} bs=1M'.format(volume))
        if rslt.succeeded:
            puts("yer disk {} has been spooned on a bear-skin rug in front of a fireplace... it's ready for your use".format(volume))
            return True
        else:
            return False