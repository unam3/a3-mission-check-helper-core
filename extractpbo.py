#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re, sys, os, exceptions
from subprocess import check_output, CalledProcessError, STDOUT

# $1 is first argument to this script as in example above

class ExtractpboError(exceptions.Exception):

    def __init__(self, value):

        self.value = value

    def __str__(self):

        return repr(self.value)

def extract_pbo(path_to_uploaded_file, additional_path=''):

    #print path_to_uploaded_file

    #print os.getcwd()

    extractpbo_output = ''

    with open(os.devnull, 'w') as f:

        # error.returncode == 1:
        # - empty file
        # - not pbo at all
        try:

            extractpbo_output = check_output(
                [
                    'extractpbo',
                    path_to_uploaded_file
                ],
                stderr=STDOUT
            )

        except CalledProcessError as error:

            #raise ExtractpboError('Wrong or corrupted file: %s for %s' % (error.returncode, path_to_uploaded_file))
            raise ExtractpboError('Wrong or corrupted file.')


    extractpbo_output_strings = extractpbo_output.split('\n')

    print [extractpbo_output_strings, len(extractpbo_output_strings), extractpbo_output_strings]

    if (len(extractpbo_output_strings) > 1 and extractpbo_output_strings[-2] != "No Error(s)"):

        raise ExtractpboError(extractpbo_output)
