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

from fabric.tasks import Task
from fabric.api import task, parallel, env
from fabric.utils import *
import acky.aws as ak

class AwsTask(Task):
    """This class is used to connect with aws; the task creates env.aws_connection based on the Acky API"""

    def __init__(self, func, *args, **kwargs):
        super(AwsTask, self).__init__(*args, **kwargs)
        # Don't use getattr() here -- we want to avoid touching self.name
        # entirely so the superclass' value remains default.
        if hasattr(func, '__name__'):
            if self.name == 'undefined':
                self.__name__ = self.name = func.__name__
            else:
                self.__name__ = self.name
        if hasattr(func, '__doc__'):
            self.__doc__ = func.__doc__
        if hasattr(func, '__module__'):
            self.__module__ = func.__module__
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        try:
            ('connecting to {0} {1}'.format(env.aws_region, env.aws_profile))
            env.aws_connection = self._aws_connect(env.aws_region, env.aws_profile)
        except:
            abort('Error configuring connection for AwsTask: {0}'.format(self.__name__))
        print env.aws_connection
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            warn("error executing {0}: {1}".format(self.__name__, e))

    def __getattr__(self, k):
        return getattr(self.func, k)

    def __details__(self):
        return get_task_details(self.func)

    def _aws_connect(self, profile, region):
        try:
            connection = ak.AWS(region, profile)
        except Exception as e:
            abort('connection error!  message: {0}'.format(e))
        else:
            return connection