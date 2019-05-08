#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import exceptions
from subprocess import check_output, CalledProcessError, STDOUT

class ExtractpboError(exceptions.Exception):

    def __init__(self, value):

        self.value = value

    def __str__(self):

        return repr(self.value)

def extract_pbo(path_to_uploaded_file):

    #print path_to_uploaded_file

    extractpbo_output = ''

    try:

        extractpbo_output = check_output(
            [
                'extractpbo',
                path_to_uploaded_file
            ],
            stderr=STDOUT
        )

    # error.returncode == 1:
    # - empty file
    # - not pbo at all
    except CalledProcessError as error:

        #raise ExtractpboError('Wrong or corrupted file: %s for %s' % (error.returncode, path_to_uploaded_file))
        raise ExtractpboError('Wrong or corrupted file.')


    extractpbo_output_strings = extractpbo_output.split('\n')

    print [extractpbo_output_strings, len(extractpbo_output_strings), extractpbo_output_strings]

    if (len(extractpbo_output_strings) > 1 and extractpbo_output_strings[-2] != "No Error(s)"):

        raise ExtractpboError(extractpbo_output)
