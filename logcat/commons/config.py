#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import xml.dom.minidom


class InvalidConfigException(Exception):
    """
    Exception raised by failures in configuration.
    """
    pass


class HostConfig(object):

    def __init__(self, ip_address=None, port=22, username=None, password=None, timeout=5, props=None):
        self._ip_address = ip_address
        self._port = port
        self._username = username
        self._password = password
        self._timeout = timeout
        if props is None:
            self._props = {}
        else:
            self._props = props

    def get_ip_address(self):
        return self._ip_address

    def set_ip_address(self, ip_address):
        self._ip_address = ip_address

    def get_port(self):
        return self._port

    def set_port(self, port):
        self._port = port

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def get_timeout(self):
        return self._timeout

    def set_timeout(self, timeout):
        self._timeout = timeout

    def get_all_props(self):
        return self._props

    def put_multi_props(self, props):
        if (props is not None) and (len(props) > 0):
            for item in props:
                self._props[item] = props[item]

    def get_prop(self, name):
        if (name is not None) and (name in self._props):
            return self._props[name]
        else:
            return None

    def put_prop(self, name, value):
        if (name is not None) and (value is not None):
            self._props[name] = value

    def remove_prop(self, name):
        if name is not None:
            del self._props[name]


class HostConfigLoader:

    def __init__(self, path):
        self._path = path
        self.__load()

    def get_host_configs(self):
        return self._host_configs

    def reload(self):
        self.__load()

    def __load(self):
        dom = xml.dom.minidom.parse(self._path)
        root = dom.documentElement
        # globals
        globals_config = {}
        globals_elements = root.getElementsByTagName('globals')
        if len(globals_elements) > 0:
            globals_element = globals_elements[0]
            # port
            port_elements = globals_element.getElementsByTagName('port')
            if (len(port_elements) > 0) and (len(port_elements[0].childNodes) > 0) \
                    and hasattr(port_elements[0].childNodes[0], 'data'):
                port = port_elements[0].childNodes[0].data
                if len(port.strip()) == 0:
                    raise InvalidConfigException('The value of port can\'t be blank.')
                elif re.match('^[1-9][0-9]*$', port.strip()) is None:
                    raise InvalidConfigException('The value of port must be a number.')
                globals_config['port'] = int(port.strip())
            # username
            username_elements = globals_element.getElementsByTagName('username')
            if (len(username_elements) > 0) and (len(username_elements[0].childNodes) > 0) \
                    and hasattr(username_elements[0].childNodes[0], 'data'):
                username = username_elements[0].childNodes[0].data
                if len(username.strip()) == 0:
                    raise InvalidConfigException('The value of username can\'t be blank.')
                globals_config['username'] = username.strip()
            # password
            password_elements = globals_element.getElementsByTagName('password')
            if (len(password_elements) > 0) and (len(password_elements[0].childNodes) > 0) \
                    and hasattr(password_elements[0].childNodes[0], 'data'):
                password = password_elements[0].childNodes[0].data
                if len(password.strip()) == 0:
                    raise InvalidConfigException('The value of password can\'t be blank.')
                globals_config['password'] = password.strip()
            # timeout
            timeout_elements = globals_element.getElementsByTagName('timeout')
            if (len(timeout_elements) > 0) and (len(timeout_elements[0].childNodes) > 0) \
                    and hasattr(timeout_elements[0].childNodes[0], 'data'):
                timeout = timeout_elements[0].childNodes[0].data
                if len(timeout.strip()) == 0:
                    raise InvalidConfigException('The value of timeout can\'t be blank.')
                elif re.match('^[0-9]+(\\.[0-9]+)?$', timeout.strip()) is None:
                    raise InvalidConfigException('The value of port must be a float.')
                globals_config['timeout'] = float(timeout.strip())
            # props
            props_elements = globals_element.getElementsByTagName('props')
            if len(props_elements) > 0:
                props = {}
                prop_elements = props_elements[0].getElementsByTagName('prop')
                for prop in prop_elements:
                    name = prop.getAttribute('name')
                    if (name is None) or (len(name) == 0):
                        raise InvalidConfigException('The name of prop must be specified.')
                    if (len(prop.childNodes) > 0) and hasattr(prop.childNodes[0], 'data'):
                        value = prop.childNodes[0].data
                    elif prop.hasAttribute('value'):
                        value = prop.getAttribute('value')
                    else:
                        raise InvalidConfigException('The value of prop "%s" must be specified.' % name)
                    props[name] = value
                globals_config['props'] = props
        # hosts
        hosts = root.getElementsByTagName('host')
        self._host_configs = []
        for host in hosts:
            host_config = HostConfig()
            # ip_address
            ip_address_elements = host.getElementsByTagName('ip_address')
            if (len(ip_address_elements) > 0) and (len(ip_address_elements[0].childNodes) > 0) \
                    and hasattr(ip_address_elements[0].childNodes[0], 'data'):
                ip_address = ip_address_elements[0].childNodes[0].data
                if len(ip_address.strip()) == 0:
                    raise InvalidConfigException('The value of ip_address can\'t be blank.')
                host_config.set_ip_address(ip_address.strip())
            else:
                raise InvalidConfigException('ip_address must be specified.')
            # port
            port_elements = host.getElementsByTagName('port')
            if (len(port_elements) > 0) and (len(port_elements[0].childNodes) > 0) \
                    and hasattr(port_elements[0].childNodes[0], 'data'):
                port = port_elements[0].childNodes[0].data
                if len(port.strip()) == 0:
                    raise InvalidConfigException('The value of port can\'t be blank.')
                elif re.match('^[1-9][0-9]*$', port.strip()) is None:
                    raise InvalidConfigException('The value of port must be a number.')
                host_config.set_port(int(port.strip()))
            elif 'port' in globals_config:
                host_config.set_port(globals_config['port'])
            # username
            username_elements = host.getElementsByTagName('username')
            if (len(username_elements) > 0) and (len(username_elements[0].childNodes) > 0) \
                    and hasattr(username_elements[0].childNodes[0], 'data'):
                username = username_elements[0].childNodes[0].data
                if len(username.strip()) == 0:
                    raise InvalidConfigException('The value of username can\'t be blank.')
                host_config.set_username(username.strip())
            elif 'username' in globals_config:
                host_config.set_username(globals_config['username'])
            else:
                raise InvalidConfigException('username must be specified.')
            # password
            password_elements = host.getElementsByTagName('password')
            if (len(password_elements) > 0) and (len(password_elements[0].childNodes) > 0) \
                    and hasattr(password_elements[0].childNodes[0], 'data'):
                password = password_elements[0].childNodes[0].data
                if len(password.strip()) == 0:
                    raise InvalidConfigException('The value of password can\'t be blank.')
                host_config.set_password(password.strip())
            elif 'password' in globals_config:
                host_config.set_password(globals_config['password'])
            else:
                raise InvalidConfigException('password must be specified.')
            # timeout
            timeout_elements = host.getElementsByTagName('timeout')
            if (len(timeout_elements) > 0) and (len(timeout_elements[0].childNodes) > 0) \
                    and hasattr(timeout_elements[0].childNodes[0], 'data'):
                timeout = timeout_elements[0].childNodes[0].data
                if len(timeout.strip()) == 0:
                    raise InvalidConfigException('The value of timeout can\'t be blank.')
                elif re.match('^[0-9]+(\\.[0-9]+)?$', timeout.strip()) is None:
                    raise InvalidConfigException('The value of port must be a float.')
                host_config.set_timeout(float(timeout.strip()))
            elif 'timeout' in globals_config:
                host_config.set_timeout(globals_config['timeout'])
            # props
            props_elements = host.getElementsByTagName('props')
            if len(props_elements) > 0:
                prop_elements = props_elements[0].getElementsByTagName('prop')
                for prop in prop_elements:
                    name = prop.getAttribute('name')
                    if (name is None) or (len(name) == 0):
                        raise InvalidConfigException('The name of prop must be specified.')
                    if (len(prop.childNodes) > 0) and hasattr(prop.childNodes[0], 'data'):
                        value = prop.childNodes[0].data
                    elif prop.hasAttribute('value'):
                        value = prop.getAttribute('value')
                    else:
                        raise InvalidConfigException('The value of prop "%s" must be specified.' % name)
                    host_config.put_prop(name, value)
            if 'props' in globals_config:
                host_props = host_config.get_all_props()
                for key, value in globals_config['props'].items():
                    if key not in host_props:
                        host_config.put_prop(key, value)
            self._host_configs.append(host_config)
