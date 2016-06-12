#!/usr/bin/python
# -*- coding: utf-8 -*-

from commons.config import InvalidConfigException
from logcat import Logcat


class BusyBox(object):

    def __init__(self, host_config):
        if host_config is None:
            raise ValueError('host_config can\'t be None.')
        else:
            self._host_config = host_config
            self._logcat = Logcat(host_config)

    def exec_task(self, task_id, args):
        if (task_id is None) or (len(task_id) == 0):
            raise ValueError('The value of task_name can\'t be None or blank.')
        # Get the command
        cmd_key = 'logcat.busybox.' + task_id + '.command'
        cmd_val = self._host_config.get_prop(cmd_key)
        if cmd_val is None:
            raise InvalidConfigException(
                    'prop \'%s\' is not specified for host %s.' % (cmd_key, self._host_config.get_ip_address()))
        elif len(cmd_val.strip()) == 0:
            raise InvalidConfigException(
                    'prop \'%s\' can\'t be blank for host %s.' % (cmd_key, self._host_config.get_ip_address()))
        else:
            cmd_val = cmd_val.strip()
        if (args is not None) and (len(args) > 0):
            cmd = cmd_val.format(args=args)
        else:
            cmd = cmd_val
        # Get the working directory if exists
        path = self._host_config.get_prop('logcat.busybox.' + task_id + '.path')
        if (path is not None) and (len(path.strip()) > 0):
            path = path.strip()
        else:
            path = None
        self._logcat.exec_cmd(path, cmd)
