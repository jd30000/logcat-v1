#!/usr/bin/python
# -*- coding: utf-8 -*-


class StringUtils(object):

    @staticmethod
    def is_empty(s):
        return (s is None) or (len(s) == 0)

    @staticmethod
    def is_not_empty(s):
        return not StringUtils.is_empty(s)

    @staticmethod
    def is_blank(s):
        return (s is None) or (len(s.strip()) == 0)

    @staticmethod
    def is_not_blank(s):
        return not StringUtils.is_blank(s)

    @staticmethod
    def is_not_blank(s):
        return not StringUtils.is_blank(s)

    @staticmethod
    def equals_ignore_case(s1, s2):
        if (s1 is not None) and (s2 is not None):
            return cmp(s1.upper(), s2.upper()) == 0
        else:
            return (s1 is None) and (s2 is None)
