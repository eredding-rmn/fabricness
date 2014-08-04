fabricness
==========
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
      ____   __    ___   ___   _   __    _      ____  __   __
     | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
     |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  basic fabric tasks for productivity

# installation

    $ git clone <this repo>

    $ cd <this repo>; pip install -r requirements.txt

    $ cd fabricness

    $ #profit


# usage

    $ fab -l


# further question

    $ fab -d <method listed in fab -l>


# even further questions

    $ echo "$YOUR_QUESTION" > /dev/louder

# an example:

    $ fab profile:production region:us-east-1 set_hosts_by_ident:my-special-hosts util.command:w

# contributing

## guidelines-ish
* add as little as possible to the base fabfile

* when adding a new set of tasks for a service or some logical grouping:

    * add a folder in the root directory

    * add __init__.py

    * as you build out tasks that are visible, and decorated as such, add the task name in __all__; this is how your task is exposed

    * Make sure it has the header:


          # -*- coding: UTF-8 -*-
          # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
          #  ____   __    ___   ___   _   __    _      ____  __   __
          # | |_   / /\  | |_) | |_) | | / /`  | |\ | | |_  ( (` ( (`
          # |_|   /_/--\ |_|_) |_| \ |_| \_\_, |_| \| |_|__ _)_) _)_)
          # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
          #  basic fabric tasks for productivity; in this case:

          from common import *

          __all__ = []


* if it uses some python libraries elsewhere, make a helper function
 in lib that includes it during the call; don't blanket include
 an external library *if possible* (sometimes, it's not)

* tasks without doc strings are the reason why babies cry

* handle input verification with handling TypeError exceptions (an attempt to be pythonic)

* I know, it's fabric, but lets try to only print what's necessary; we can help each other as we build this

* The order of imports in common matters.  *shrugs*

* ALWAYS ALWAYS ALWAYS RETURN A VALUE!  Without returning a value, your task can sit there forever and never return.  It's stupid, but it happens.

