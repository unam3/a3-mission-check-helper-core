#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import exceptions
from subprocess import call

def remove_check_products(path_to_delete_some):

    call(
        [
            'rm',
            '-r',
            '-f',
            path_to_delete_some
        ]
    )
