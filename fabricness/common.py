# -*- coding: UTF-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ____   __    ___   ___   _   __    _      ____  __   __
# | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
# |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  basic fabric tasks for productivity

from fabric.api import *
from fabric.colors import *
import os
import sys
import re
import datetime
from string import ascii_lowercase
from collections import deque
import uuid
from sys import exit

########### Fabric Settings
env.use_ssh_config = True
env.warn_only = True
env.forward_agent = True
env.connection_attempts = 2
env.skip_bad_hosts = True
env.colorize_errors = True
env.my_poll_timeout = 780
env.my_sleep = 5
env.abort_on_prompts = True

env.aws_connection = None

env.host_aliases = {}

env.template_dir = "templates"
env.LOGDIR = "logs"
env.INSTALLER = "apt-get "
env.gateway_host_ident = 'eop-sec-prt-001'

import lib
import util
import service
from lib.stfutask import StfuTask
from lib.awstask import AwsTask
### import some local libraries
import apt
import cpu
import disk
import fluentd
import network
import puppet
import sensu
import disk.mdadm as mdadm
import disk.ebs as ebs
