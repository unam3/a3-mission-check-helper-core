#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals


def was_mission_binarized(mission_sqm_path):

    reference_line_part = '//DeRap: wog_'

    with open(mission_sqm_path, 'r') as f:
    
        for i, line in enumerate(f):
            
            # we interested only in second line with signature
            if (i == 1):
                
                #print line

                #for n, word in enumerate(line):
                #    
                #    print n, word, reference_line_part[n], word == reference_line_part[n]

                return line.startswith(reference_line_part)
