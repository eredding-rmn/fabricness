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
from fabric.api import task, parallel
from fabric.utils import *

class StfuTask(Task):
    """This is a task that tries to shut everything up"""

    def __init__(self, func, *args, **kwargs):
        super(StfuTask, self).__init__(*args, **kwargs)
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
            return self.func(*args, **kwargs)
        except Exception as e:
            warn("error executing {0}: {1}".format(self.__name__, e))

    def __getattr__(self, k):
        return getattr(self.func, k)

    def __details__(self):
        return get_task_details(self.func)
