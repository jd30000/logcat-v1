#!/usr/bin/python
# -*- coding: utf-8 -*-

from commons.ssh import CommandExecutor, CommandCallback
import codecs


class LogCat(object):

    def __init__(self, host_config):
        if host_config is None:
            raise ValueError('host_config can\'t be None!')
        else:
            self._host_config = host_config
            ip_address = host_config.get_ip_address()
            port = host_config.get_port()
            if port is None:
                port = 22
            username = host_config.get_username()
            password = host_config.get_password()
            timeout = host_config.get_timeout()
            if timeout is None:
                timeout = 5
            self._cmd_executor = CommandExecutor(ip_address, port, username, password, timeout)

    def __format_log_results(self, lines):
        text = ''
        if len(lines) > 0:
            title = '------------------------------- Host: %s ' % self._host_config.get_ip_address()
            title = title.ljust(80, '-')
            title += '\n'
            text += title
            for line in lines:
                text += line
        return text

    def __write_to_file(self, lines, output_file):
        with codecs.open(output_file, 'a', 'utf-8') as out:
            data = self.__format_log_results(lines)
            out.write(data)

    def __print_to_console(self, lines):
        print(self.__format_log_results(lines))

    def exec_cmd(self, pwd, cmd, output_file, size):
        if (pwd is None) or (len(pwd.strip()) == 0):
            pwd = '~'
        else:
            pwd = pwd.strip()
        if (cmd is None) or (len(cmd.strip()) == 0):
            raise ValueError('The command to be executed can\'t be None or blank!')
        else:
            cmd = cmd.strip()
        if output_file is not None:
            output_file = output_file.strip()
            if len(output_file) == 0:
                raise ValueError('The path of output_file can\'t be blank!')
        cmd = ('cd ' + pwd + '; ' + cmd)
        lines = []
        self._cmd_executor.exec_command(cmd, LogCatCommandCallback(lines, size))
        if output_file is None:
            self.__print_to_console(lines)
        else:
            self.__write_to_file(lines, output_file)


class LogCatCommandCallback(CommandCallback):

    def __init__(self, lines, size):
        if lines is None:
            raise ValueError('lines reference can\'t be None!')
        self._lines = lines
        self._size = size

    def __is_continuous(self):
        if self._size is not None:
            return len(self._lines) < self._size
        return True

    def handle(self, stdin, stdout, stderr):
        while self.__is_continuous():
            line = stdout.readline()
            if len(line) <= 0:
                break
            self._lines.append(line)
