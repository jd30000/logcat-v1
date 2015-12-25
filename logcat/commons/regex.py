#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


class RegexUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def escape_regex_specials(s):
        if s is None:
            return None
        pattern = re.compile('(\\.|\\$|\\[|\\]|\\^|\\*|\\+|\\{|\\}|\\(|\\)|\\\\|\\?|\\|)')
        return pattern.sub(lambda matches: '\\' + matches.group(0), s)
