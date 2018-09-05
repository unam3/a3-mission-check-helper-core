#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re

with open('/home/yay/a3/wog_96_the_forgotten_war_latest.lingor3/mission.sqm') as opened_mission_file:
    #print opened_mission_file

    mission_class_marker = str('class Mission')

    #print mission_class_marker

    class_path = []

    loop_into_mission_class = False

    for line in opened_mission_file:
        if (line.startswith(mission_class_marker)):
            loop_into_mission_class = True

        if (loop_into_mission_class):
            #print line

            if (re.match('\s*class', line) and not line.endswith('{};\r\n')):
                class_name = line.split('class ')[1][:-2]

                class_path.append(class_name)

                #print 'classname is', class_name

                #print class_path

            elif (re.match('\s*};', line)):
                class_path.pop()

                #print class_path

            elif (class_name == 'Intel'):
                splitted_attribute_definition = line.strip().decode('utf-8').split(' = ')

                #print splitted_attribute_definition
                
                if (len(splitted_attribute_definition) == 2):
                    attr_name, attr_value = splitted_attribute_definition

                    # in the mission file strings strings are in quotes, ends with semi
                    stripped_attr_value = attr_value[1:-2]

                    if (attr_name == 'briefingName'):
                        # 2
                        if (not re.match('WOG \d{2,3} (\w+\ )+\d\.\d$', stripped_attr_value, re.UNICODE)):
                            print 'Название миссии не удовлетворяет шаблону.'.encode('utf-8')

                        # 2.1
                        #if (not stripped_attr_value.startswith('WOG ')):
                        #    #print ('Название миссии должно начинаться с "WOG".'.encode('utf-8')
                        #    print ('Название миссии должно начинаться с "WOG". (%s)' % (stripped_attr_value)).encode('utf-8'),

                        #if (attr_value.decode('utf-8').split(' ')):
                            

                    #if (attr_name == 'overviewText'):
                        #print attr_name, attr_value.encode('utf-8')
