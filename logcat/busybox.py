#!/usr/bin/python
# -*- coding: utf-8 -*-

from commons.config import InvalidConfigException
from logcat import LogCat
import re


class BusyBox(object):

    def __init__(self, host_config):
        if host_config is None:
            raise ValueError('host_config can\'t be None!')
        else:
            self._host_config = host_config
            self._logcat = LogCat(host_config)

    def print_md5sum(self):
        files_val = self._host_config.get_prop('logcat.busybox.md5sum.files')
        if files_val is None:
            raise InvalidConfigException('prop logcat.busybox.md5sum.files is not specified for host %s!' %
                                         self._host_config.get_ip_address())
        elif len(files_val.strip()) == 0:
            raise InvalidConfigException('prop logcat.busybox.md5sum.files can\'t be blank for host %s!' %
                                         self._host_config.get_ip_address())
        else:
            files_val = files_val.strip()
        files = files_val.split(',')
        cmd = 'md5sum'
        for f in files:
            cmd += (' ' + f.strip())
        self._logcat.exec_cmd(cmd=cmd)

    def grep(self, keyword):
        if (keyword is None) or (len(keyword) == 0):
            raise ValueError('The value of keyword can\'t be None or blank!')
        files_val = self._host_config.get_prop('logcat.busybox.grep.files')
        if files_val is None:
            raise InvalidConfigException('prop logcat.busybox.grep.files is not specified for host %s!' %
                                         self._host_config.get_ip_address())
        elif len(files_val.strip()) == 0:
            raise InvalidConfigException('prop logcat.busybox.grep.files can\'t be blank for host %s!' %
                                         self._host_config.get_ip_address())
        else:
            files_val = files_val.strip()
        files = files_val.split(',')
        cmd = 'grep ' + keyword
        for f in files:
            cmd += (' ' + f.strip())
        self._logcat.exec_cmd(cmd=cmd)

    def print_db_conn(self):
        port = self._host_config.get_prop('logcat.busybox.db-conn.port')
        if port is None:
            raise InvalidConfigException('prop logcat.busybox.db-conn.port is not specified for host %s!' %
                                         self._host_config.get_ip_address())
        elif len(port.strip()) == 0:
            raise InvalidConfigException('prop logcat.busybox.db-conn.port can\'t be blank for host %s!' %
                                         self._host_config.get_ip_address())
        elif re.match('^[1-9][0-9]*$', port.strip()) is None:
            raise InvalidConfigException('The value of prop logcat.busybox.db-conn.port must be a number for host %s!' %
                                         self._host_config.get_ip_address())
        else:
            port = port.strip()
        cmd = 'netstat -ano | grep :%s | wc -l' % port
        self._logcat.exec_cmd(cmd=cmd)

    def exec_custom_task(self, task_name, args):
        if (task_name is None) or (len(task_name) == 0):
            raise ValueError('The value of task_name can\'t be None or blank!')
        cmd_key = 'logcat.busybox.' + task_name + '.command'
        cmd_val = self._host_config.get_prop(cmd_key)
        if cmd_val is None:
            raise InvalidConfigException('prop %s is not specified for host %s!' % (cmd_key,
                                                                                    self._host_config.get_ip_address()))
        elif len(cmd_val.strip()) == 0:
            raise InvalidConfigException('prop %s can\'t be blank for host %s!' % (cmd_key,
                                                                                   self._host_config.get_ip_address()))
        else:
            cmd_val = cmd_val.strip()
        if (args is not None) and (len(args) > 0):
            cmd = cmd_val.format(args=args)
        else:
            cmd = cmd_val
        path = self._host_config.get_prop('logcat.busybox.' + task_name + '.path')
        if (path is not None) and (len(path.strip()) > 0):
            path = path.strip()
        else:
            path = None
        self._logcat.exec_cmd(path, cmd)
