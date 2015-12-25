#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import paramiko
from paramiko.ssh_exception import SSHException


class CommandExecutor(object):

    def __init__(self, ip_address, port=22, username=None, password=None, timeout=5):
        self._ip_address = ip_address
        self._port = port
        self._username = username
        self._password = password
        self._timeout = timeout

    def exec_command(self, cmd, cmd_callback):
        ssh_client = None
        args = {'cmd': cmd, 'cmd_callback': cmd_callback}
        try:
            ssh_client = self.__get_ssh_client()
            self.__exec_command(ssh_client, args)
        except SSHException as e:
            print('Failed to execute the command "%s" at host %s, Exception: %s' % (args['cmd'],
                                                                                    self._ip_address,
                                                                                    e.message))
        finally:
            if ssh_client is not None:
                ssh_client.close()

    def exec_multi_commands(self, cmds, cmd_callbacks):
        if (cmds is not None) or (len(cmds) > 0):
            ssh_client = None
            args = {'cmd': None, 'cmd_callback': None}
            try:
                ssh_client = self.__get_ssh_client()
                for index in range(0, len(cmds)):
                    args = {'cmd': cmds[index], 'cmd_callback': cmd_callbacks[index]}
                    self.__exec_command(ssh_client, args)
            except SSHException as e:
                if args['cmd'] is None:
                    print('Failed to connect host %s, Exception: %s' % (self._ip_address, e.message))
                else:
                    print('Failed to execute the command "%s" at host %s, Exception: %s' % (args['cmd'],
                                                                                            self._ip_address,
                                                                                            e.message))
            finally:
                if ssh_client is not None:
                    ssh_client.close()

    def __exec_command(self, ssh_client, args):
        stdin, stdout, stderr = ssh_client.exec_command(args['cmd'])
        if (args['cmd_callback'] is not None) and isinstance(args['cmd_callback'], CommandCallback):
            args['cmd_callback'].handle(stdin, stdout, stderr)
            if isinstance(args['cmd_callback'], CommandCallbackChain):
                while args['cmd_callback'].has_next():
                    args['cmd'] = args['cmd_callback'].get_next_command()
                    args['cmd_callback'] = args['cmd_callback'].get_next_command_callback()
                    self.__exec_command(ssh_client, args)

    def __get_ssh_client(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self._ip_address, self._port, self._username, self._password, timeout=self._timeout)
        return ssh_client


class CommandCallback(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, stdin, stdout, stderr):
        """
        Handle the stdin, stdout, and stderr of the executing command

        :param object stdin: standard input file object
        :param object stdout: standard output file object
        :param object stderr: standard error object
        """
        pass


class CommandCallbackChain(CommandCallback):

    def __init__(self):
        self._next_command = None
        self._next_command_callback = None

    @abstractmethod
    def handle(self, stdin, stdout, stderr):
        pass

    def get_next_command(self):
        return self._next_command

    def get_next_command_callback(self):
        return self._next_command_callback

    def set_next(self, next_command, next_command_callback=None):
        self._next_command = next_command
        if next_command_callback is not None:
            if isinstance(next_command_callback, CommandCallback):
                self._next_command_callback = next_command_callback
            else:
                raise TypeError(
                    'next_command_callback must be instance of logcat.commons.ssh.CommandCallback '
                    'or logcat.commons.ssh.CommandCallbackChain!')

    def has_next(self):
        return self._next_command is not None
