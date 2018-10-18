#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re, sys

path_to_mission_sqm = sys.argv[1]

with open(path_to_mission_sqm) as opened_mission_file:
    #print opened_mission_file

    sides = {}

    class_path = []

    in_group_class = False

    group_side = False

    in_unit_class = False
    
    #in_unit_custom_attrs = False

    in_unit_custom_attrs_medic = False

    in_unit_custom_attrs_engineer = False

    in_group_custom_attrs = False

    for line in opened_mission_file:
        #print line
        #print len(class_path), class_path

        if (re.match('\s*class ', line) and not line.endswith('{};\r\n')):
            class_name = line.split('class ')[1][:-2]

            class_path.append(class_name)

            #print 'classname is', class_name

            #print class_path

        elif (re.match('\s*};', line)):
            if (in_group_class and len(class_path) == 3):

                in_group_class = False

                group_side = False

            if (in_unit_class and not (in_group_class and len(class_path) >= 5)):

                in_unit_class = False

            #if (in_unit_custom_attrs and len(class_path) == 6):

            #    in_unit_custom_attrs = False

            if (in_unit_custom_attrs_medic and len(class_path) == 7):

                in_unit_custom_attrs_medic = False

            if (in_unit_custom_attrs_engineer and len(class_path) == 7):

                in_unit_custom_attrs_engineer = False

            class_path.pop()

            #print class_path

        elif (len(class_path)):
            splitted_attribute_definition = line.strip().decode('utf-8').split(' = ')

            if (len(splitted_attribute_definition) == 2):
                attr_name, attr_value = splitted_attribute_definition

                # in the mission file strings strings are in quotes, ends with semi
                stripped_attr_value = attr_value[1:-2]

                stripped_semi_attr_value = attr_value[:-1]

                #general attr
                if (class_path[0] == str('ScenarioData')):
                    if (attr_name == 'author'):
                        print 'Author:', stripped_attr_value

                    if (attr_name == 'loadScreen'):
                        print 'Load screen image:', stripped_attr_value

                    if (attr_name == 'saving' and stripped_semi_attr_value != '0'):
                        print 'Сохранение должно быть выключено.'.encode('utf-8')

                    if (attr_name == 'respawn' and stripped_semi_attr_value != '1'):
                        print 'Respawn must be set to "Spectator".'

                elif (class_path[0] == str('CustomAttributes')):

                    #general attr
                    if ((len(class_path) == 6 and class_path[1] == 'Category0' and class_path[2] == 'Attribute0'
                        and class_path[3] == 'Value' and class_path[4] == 'data' and class_path[5] == 'value' 
                        and attr_name == 'items' and stripped_semi_attr_value != str(1))
                        or (len(class_path) == 8 and class_path[1] == 'Category0' and class_path[2] == 'Attribute0'
                        and class_path[3] == 'Value' and class_path[4] == 'data' and class_path[5] == 'value'
                        and class_path[6] == 'Item0' and class_path[7] == 'data'
                        and attr_name == 'value' and stripped_attr_value != 'Spectator')):

                            print 'Only "Spectator" option must be set in the "Rulesets" of the "Multiplayer" attributes'
                    #general attr
                    if (len(class_path) == 3 and class_path[1] == 'Category1' and class_path[2] == 'Attribute0'
                        and attr_name == 'property' and stripped_attr_value != 'EnableTargetDebug'):

                            print 'Please turn on "Enable Target Debugging"'

                elif (class_path[0] == str('Mission')):

                    if (class_name == 'Intel'):
                        #print splitted_attribute_definition
                        
                        if (attr_name == 'briefingName'):
                            print 'Mission name:', attr_value

                            # 2
                            if (not re.match('WOG \d{2,3} (\w+\ )+\d\.\d$', stripped_attr_value, re.UNICODE)):
                                print 'Название миссии не удовлетворяет шаблону.'.encode('utf-8')

                            # 2.1
                            #if (not stripped_attr_value.startswith('WOG ')):
                            #    #print ('Название миссии должно начинаться с "WOG".'.encode('utf-8')
                            #    print ('Название миссии должно начинаться с "WOG". (%s)' % (stripped_attr_value)).encode('utf-8'),

                            #if (attr_value.decode('utf-8').split(' ')):
                                
                        # side (color, attack) - side (color, def)
                        elif (attr_name == 'overviewText'):
                            print stripped_attr_value.encode('utf-8')

                        elif ((attr_name == 'startWind' or attr_name == 'forecastWind')
                            and float(stripped_semi_attr_value) > 0.4):

                            print 'Wind must be less than or equal to 40%:', int(float(stripped_semi_attr_value) * 100)

                        elif ((attr_name == 'startRain' or attr_name == 'forecastRain')
                            and float(stripped_semi_attr_value) > 0.4):
                            print 'Rain must be less than or equal to 40%:', int(float(stripped_semi_attr_value) * 100)

                    elif (len(class_path) >= 2 and class_path[1] == str('Entities')):

                        # Mission - Entities - ItemN /w dataType = "Group"
                        # parse "side" property too
                        if (len(class_path) == 3):

                            if (attr_name == 'dataType' and stripped_attr_value == 'Group'):

                                in_group_class = True

                            elif (attr_name == 'side' and not (stripped_attr_value == 'West'
                                or stripped_attr_value == 'East' or stripped_attr_value == 'Independent')):

                                group_side = stripped_attr_value

                                if (not sides.get(group_side)):
                                    sides[group_side] = []

                                # add empty list for the group units
                                sides[group_side].append([])

                                print 'new group'

                        # last part for additional filtering
                        elif (not in_unit_class and in_group_class and group_side):
                            # Mission → Entities → ItemN /w dataType == 'Group' → Entities → ItemN
                            if (len(class_path) == 5 and attr_name == 'dataType'
                                and stripped_attr_value == 'Object'):

                                # add empty unit dict to the last group units list
                                sides[group_side][-1].append({})

                                in_unit_class = True

                            # Mission → Entities → ItemN /w dataType == 'Group' → CustomAttributes
                            #    → AttributeN /w property == "groupID" - Value - data - 'value' property
                            #elif (len(class_path) == 5 and class_path[4] == 'CustomAttributes'):
                                #and attr_name == 'property'):# and stripped_attr_value == 'groupID'):
                            #else:

                            #    print 2323, in_unit_class, line
                                #in_group_custom_attrs = True

                            # Mission - Entities - ItemN /w dataType = "Group" - CustomAttributes - AttributeN /w property == "groupID" - Value - data - 'value' property
                            #elif (in_group_custom_attrs and len(class_path) == 7 and attr_name == 'value'):

                                #print 'l\n', line, '\nl'
                        
                        elif (in_unit_class):

                            # parse "side" property too. just in case

                            if (attr_name == 'init' or attr_name == 'description' or attr_name == 'type'):

                                #print stripped_attr_value

                                sides[group_side][-1][-1][attr_name] = stripped_attr_value
                            
                            # isPlayable propert present only if slot is playable 
                            elif (attr_name == 'isPlayable' and stripped_semi_attr_value != '1'):

                                print 'slot is not playable!'

                            #print class_path

                            #print line

                            # Mission - Entities - ItemN /w dataType = "Group" - Entities - ItemN - CustomAttributes
                            elif (len(class_path) == 7 and class_path[5] == 'CustomAttributes'
                                and attr_name == 'property'):

                                if (stripped_attr_value == 'ace_isMedic'):

                                    in_unit_custom_attrs_medic = True

                                elif (stripped_attr_value == 'ace_isEngineer'):

                                    in_unit_custom_attrs_engineer = True

                            elif (in_unit_custom_attrs_medic and len(class_path) == 9 and class_path[7] == 'Value'
                                and class_path[8] == 'data'):

                                #print class_path, len(class_path)

                                #print 'ace_isMedic', stripped_semi_attr_value
                                
                                sides[group_side][-1][-1]['ace_isMedic'] = stripped_semi_attr_value

                            elif (in_unit_custom_attrs_engineer and len(class_path) == 9 and class_path[7] == 'Value'
                                and class_path[8] == 'data'):

                                #print 'ace_isEngineer', stripped_semi_attr_value

                                sides[group_side][-1][-1]['ace_isEngineer'] = stripped_semi_attr_value

                            #print class_path
                            #print line

                        #if (len(class_path) == 7 and class_path[3] == 'CustomAttributes'
                        #    and class_path[5] == 'Value' and class_path[6] == 'data' and attr_name == 'value'):

    print sides
