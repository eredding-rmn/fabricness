# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity; in this case: utity!
#
#  If you find yourself repeating some sort of general form,
#   make it a utility function today!
#

from common import *
from lib.stfutask import StfuTask
from lib.awstask import AwsTask

__all__ = [
    'get_processorcount',
    'get_physicalprocessorcount',
    'get_osfamily',
    'resolve_installer',
    'install_package',
    'command',
    'sudo_command',
    'check_for_binary',
    'pgrep',
    'dpkg_grep',
    'testing'
]

@task
@parallel
def get_processorcount():
    '''
    return the processor count via facter

    '''
    rslt = sudo_command("facter processorcount")
    if rslt.succeeded:
        return int(rslt)
    else:
        return None


@task
@parallel
def get_physicalprocessorcount():
    '''
    return the physicalprocessorcount count via facter

    '''
    rslt = sudo_command("facter physicalprocessorcount")
    if rslt.succeeded:
        return int(rslt)
    else:
        return None


@task
@parallel
def get_osfamily():
    '''
    return os family via facter

    '''
    rslt = run("facter osfamily")
    if rslt.succeeded:
        return "{}".format(rslt)
    else:
        return None


@parallel
def resolve_installer():
    '''
    figure out if we use yum or apt
    '''
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
    '''
    install a package on a host

    Args:
        command:package
    '''
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

    Args:
        command:string
    '''
    with settings(warn_only=True):
        return run("%s" % command)


@task
@parallel
def sudo_command(command):
    '''
    run an arbitrary sudo command; intended for use from within fabric
      because it will bust up cli arguments into a list

    Args:
        binary_name:string
    '''
    with settings(warn_only=True):
        return sudo(command)


@task
@parallel
def check_for_binary(binary_name):
    '''
    check for a binary via 'which' command

    Args:
        binary_name:string
    '''
    with hide('everything'):
        we_good = run('which {}'.format(binary_name))
        if we_good.succeeded:
            return True
        else:
            return False


@task(task_class=StfuTask)
@parallel
def pgrep(binary_name=None, user=None):
    '''
    run pgrep for a binary; can specify binary_name or user for filtering

    Args:
        binary_name:string
        user: string
    '''
    b_arg = ''
    u_arg = ''
    try:
        if binary_name:
            b_arg = " -f {0} ".format(binary_name)
            term = binary_name
        if user:
            u_arg = " -u {0}".format(user)
            term = user
        cmd = 'pgrep -o {0} {1}'.format(u_arg, b_arg)
    except TypeError as e:
        warn('invalid arguments: {0}'.format(e.message))
    else:
        rslt = command(cmd)
        if rslt.succeeded:
            print(
                '> {0} :: Found process based on {1}: {2}'.format(
                    env.host_string, term, rslt
                )
            )
            return rslt
        else:
            return None


@task
@parallel(pool_size=7)
def dpkg_grep(package):
    m = re.compile(package)
    with hide('everything'):
        rslt = sudo('dpkg -l |grep {0}'.format(package))
        if rslt.succeeded:
            if m.search(rslt):
                return True
            else:
                return False



@task(task_class=AwsTask)
def testing():
    '''
    Stub debug task for outputting all that it knows...
    '''
    print 'dir {0}'.format(dir())
    print 'env {0}'.format(env)
    puts('yay: '.format(env.aws_connection))
    pass