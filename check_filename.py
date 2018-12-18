#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re


def is_filename_ok(filename):

        if re.match('^wog_\d{2,3}_[a-z0-9_]+_[1-9][0-9]\.[A-Za-z0-9_]+\.pbo$', filename, re.UNICODE):

            return True


def run_tests():

    test_filenames = [
        "pluh",
        " wog_156_voshod_10.Takistan.pbo",
        "wog_156_voshod_10.Takistan.pbo ",
        "wog156_voshod_10.Takistan.pbo",
        "wog_5_voshod_10.Takistan.pbo",
        "wog_56_.10.Takistan.pbo",
        "wog_56_voshod.10.Takistan.pbo",
        "wog_56_voshod_01.Takistan.pbo",
        "wog_56_voshod_109.Takistan.pbo",
        "wog_56_voshod_10_Takistan.pbo",
        "wog_56_voshod_10.Taki.stan.pbo"
    ]

    for i, filename in enumerate(test_filenames):
        
        if is_filename_ok(filename):

            return False

    #print 'check_filename tests passed'

    return True

#print run_tests()
