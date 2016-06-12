#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from commons.config import HostConfigLoader, InvalidConfigException
from commons.lang import StringUtils
from logcat import Logcat
from busybox import BusyBox
import os
import re
import sys
import time


def logcat():
    file_name = os.path.basename(sys.argv[0])
    argv = sys.argv[1:]
    # Print usage
    if len(argv) < 3:
        print('Usage: ' + file_name +
              ' APP_ID(Default|your_app_id) WORKING_DIRECTORY COMMAND [OUTPUT(.|FILE_PATH) LINE_SIZE]')
        sys.exit(0)
    # Check configuration file
    app_id = argv[0]
    if StringUtils.is_blank(app_id):
        print('The value of APP_ID can\'t be blank.')
        return -1
    app_id = app_id.strip()
    if StringUtils.equals_ignore_case(app_id, 'Default'):
        config_file = 'config/hosts.xml'
    else:
        config_file = 'config/' + app_id + '/hosts.xml'
    config_file = os.path.abspath(config_file)
    if not os.path.exists(config_file):
        print('The config file "%s" doesn\'t exist.' % config_file)
        return -1
    # Check working directory
    wk_dir = argv[1]
    if StringUtils.is_blank(wk_dir):
        print('The value of WORKING_DIRECTORY can\'t be blank.')
        return -1
    wk_dir = wk_dir.strip()
    # Check command
    cmd = argv[2]
    if StringUtils.is_blank(cmd):
        print('The value of COMMAND can\'t be blank.')
        return -1
    cmd = _decode_argv(cmd.strip())
    # Check output file
    output_file = None
    if len(argv) > 3:
        if StringUtils.is_blank(argv[3]):
            print('The path of OUTPUT can\'t be blank.')
            return -1
        if not StringUtils.equals_ignore_case(argv[3].strip(), '.'):
            output_file = argv[3].strip()
            if not os.path.isabs(output_file):
                output_file = os.path.abspath(output_file)
            if os.path.exists(output_file) and os.path.isdir(output_file):
                print('The path of OUTPUT can\'t be a directory.')
                return -1
            parent_dir = os.path.dirname(output_file)
            if not os.path.exists(parent_dir):
                os.mkdir(parent_dir)
    # Check line size
    size = None
    if len(argv) > 4:
        size_v = argv[4]
        if StringUtils.is_blank(argv[4]):
            print('The value of LINE_SIZE can\'t be blank.')
            return -1
        size_v = size_v.strip()
        if re.match('^-?[1-9]\d*|0$', size_v) is None:
            print('The value of LINE_SIZE must be an integer.')
            return -1
        size = int(size_v)
    # Back up the output file, if exists
    if (output_file is not None) and os.path.exists(output_file):
        backup_file = output_file + '.' + str(int(time.mktime(datetime.datetime.now().timetuple()))) + '.bak'
        os.renames(output_file, backup_file)
        print('The output file specified already exists, rename it to "%s".' % backup_file)
    # Load the configuration file for hosts
    try:
        host_config_loader = HostConfigLoader(config_file)
    except InvalidConfigException as e:
        print('The configuration is invalid: %s' % e.message)
        return -1
    host_configs = host_config_loader.get_host_configs()
    for host_config in host_configs:
        lc = Logcat(host_config)
        print('Execute command \'%s\' in path \'%s\' at server %s...' % (cmd, wk_dir, host_config.get_ip_address()))
        lc.exec_cmd(wk_dir, cmd, output_file, size)
    return 0


def busybox():
    file_name = os.path.basename(sys.argv[0])
    argv = sys.argv[1:]
    # Print usage
    if len(argv) < 2:
        print('Usage: ' + file_name + ' APP_ID(Default|your_app_id) TASK_ID [arg0 arg1...]')
        sys.exit(0)
    # Check configuration file
    app_id = argv[0]
    if StringUtils.is_blank(app_id):
        print('The value of APP_ID can\'t be blank.')
        return -1
    app_id = app_id.strip()
    if StringUtils.equals_ignore_case(app_id, 'Default'):
        config_file = 'config/hosts.xml'
    else:
        config_file = 'config/' + app_id + '/hosts.xml'
    config_file = os.path.abspath(config_file)
    if not os.path.exists(config_file):
        print('The config file "%s" doesn\'t exist.' % config_file)
        return -1
    # Check task ID
    task_id = argv[1]
    if StringUtils.is_blank(task_id):
        print('The value of TASK_ID can\'t be blank.')
        return -1
    task_id = task_id.strip()
    # Prepare arguments
    args = None
    if len(argv) > 2:
        args = argv[2:]
        # Decode the arguments
        for i in range(0, len(args)):
            args[i] = _decode_argv(args[i])
    # Load the configuration file for hosts
    try:
        host_config_loader = HostConfigLoader(config_file)
    except InvalidConfigException as e:
        print('The configuration is invalid: %s' % e.message)
        return -1
    host_configs = host_config_loader.get_host_configs()
    for host_config in host_configs:
        busy_box = BusyBox(host_config)
        print('Execute task \'%s\' at server %s...' % (task_id, host_config.get_ip_address()))
        try:
            busy_box.exec_task(task_id, args)
        except InvalidConfigException as e:
            print('Failed to execute task \'%s\' at server %s: %s' % (task_id, host_config.get_ip_address(), e.message))
    return 0


def _decode_argv(s):
    if sys.getdefaultencoding() == 'ascii':
        # Chinese Simplified (GB2312/GBK/gb18030)
        if re.search('[\\xa1-\\xfe]{2}', s):
            return s.decode('gb2312')
        elif re.search('[\\x40-\\x7e\\x80-\\xfe][\\x81-\\xfe]', s):
            return s.decode('gbk')
        elif re.search('([\\x81-\\xfe][\\x30-\\x39]){2}', s):
            return s.decode('gb18030')
    return s
