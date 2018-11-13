#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re, sys, os

from subprocess import call, check_output, CalledProcessError

path_to_mission_folder = sys.argv[1]

path_to_mission_sqm = path_to_mission_folder + '/mission.sqm'

devnull = open(os.devnull, 'w')

current_script_dir = os.path.dirname(os.path.abspath(__file__))


def customAttrIsMedic(isMedic):
    
    str = ''

    if (isMedic == '0.0'):
        
        str = '"None" regular unit medical abillities'

    elif (isMedic == '1.0'):
        
        str = '"Regular medic"'

    elif (isMedic == '2.0'):
        
        str = '"Doctor"'

    elif (isMedic is not None):
        
        str = 'Unusual "ace_isMedic" attribute value: %s' % (isMedic)

    return str


def customAttrIsEngineer(isEngineer):
    
    str = ''

    if (isEngineer == '0.0'):
        
        str = 'Unit Engineer abillities is off'

    elif (isEngineer == '1.0'):
        
        str = '"Engineer"'

    elif (isEngineer == '2.0'):
        
        str = '"Advanced Engineer"'

    elif (isEngineer is not None):
        
        str = 'Unusual "ace_isEngineer" attribute value: %s' % (isEngineer)

    return str


def checkVanillaEquip(relative_path):

    out = None

    init_path = path_to_mission_folder + '/' + '/'.join(
        relative_path.split('""')[1].split('\\')
    )

    try:
        out = check_output(
            [
                'grep',
                '-i',
                '-f', current_script_dir + '/V_Weapon.sqf',
                init_path
            ],
            stderr=devnull
        )

    except CalledProcessError as shi:

        if (shi.returncode != 1):

            print 'checkVanillaEquip return code:', shi.returncode, 'for', init_path

    return '' if (not out) else 'vannila items: ' + out.decode('utf-8')


def parse_vehicle_init(init):

    setVariables = init.split('this setVariable [""')

    init_options = {}
    
    # has any setVariable declaration
    if len(setVariables) > 1:

        for declaration in setVariables[1:]:

            if declaration.startswith('tf_side'):

                # tf_side"",""east""]; 
                #print declaration
                #print declaration[10:].split('""')[1]

                init_options['tf_side'] = declaration[10:].split('""')[1]

            elif declaration.startswith('WMT_Side'):

                #print 'WMT_Side'
                #print declaration
                #print declaration[11:].strip(' ').split(']')[0]

                init_options['WMT_Side'] = declaration[11:].strip(' ').split(']')[0]

    return init_options if len(init_options) else None


wmt_disable_fuel_stations = True

wmt_auto_med_provision = True

wmt_side_channel_by_lr = True


with open(path_to_mission_sqm) as opened_mission_file:
    #print opened_mission_file

    sides = {}

    vehicles = []

    class_path = []

    # units
    in_group_class = False

    group_side = False

    in_unit_class = False
    
    in_unit_custom_attrs_medic = False

    in_unit_custom_attrs_engineer = False

    in_group_custom_attr_group_id = False

    # vehicles
    in_object_class = False

    is_vehicle_class = False

    in_logic_class = False

    in_logic_class_custom_attr_disable_fuel_st = False

    in_logic_class_custom_attr_auto_med_provision = False

    in_logic_class_custom_attr_side_channel_by_lr = False

    for line in opened_mission_file:
        #print line
        #print len(class_path), class_path

        if (re.match('\s*class ', line) and not line.endswith('{};\r\n')):
            class_name = line.split('class ')[1][:-2]

            class_path.append(class_name)

            #print 'classname is', class_name

            #print class_path

        elif (re.match('\s*};', line)):
            if (in_group_class and group_side and len(class_path) == 3):

                in_group_class = False

                group_side = False

            elif (in_unit_class and len(class_path) < 6):

                in_unit_class = False

            elif (in_group_custom_attr_group_id and len(class_path) < 6):

                in_group_custom_attr_group_id = False

            elif (in_unit_custom_attrs_medic and len(class_path) == 7):

                in_unit_custom_attrs_medic = False

            elif (in_unit_custom_attrs_engineer and len(class_path) == 7):

                in_unit_custom_attrs_engineer = False

            elif (in_object_class and len(class_path) == 3):

                in_object_class = False

                is_vehicle_class = False

            elif (in_logic_class):

                if (len(class_path) == 3):

                    in_logic_class = False

                # why two line prints instead of oonly one with this condition?
                #elif (in_logic_class_custom_attr_disable_fuel_st):
                elif (len(class_path) == 5):
                    if (in_logic_class_custom_attr_disable_fuel_st):

                        in_logic_class_custom_attr_disable_fuel_st = False
    
                    elif (in_logic_class_custom_attr_auto_med_provision):

                        in_logic_class_custom_attr_auto_med_provision = False

                    elif (in_logic_class_custom_attr_side_channel_by_lr):

                        in_logic_class_custom_attr_side_channel_by_lr = False


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
                            and float(stripped_semi_attr_value) >= 0.41):

                            print 'Wind must be less than or equal to 40%:', int(float(stripped_semi_attr_value) * 100)

                        elif ((attr_name == 'startRain' or attr_name == 'forecastRain')
                            and float(stripped_semi_attr_value) >= 0.41):

                            print 'Rain must be less than or equal to 40%:', int(float(stripped_semi_attr_value) * 100)

                    elif (len(class_path) >= 2 and class_path[1] == str('Entities')):

                        # Mission - Entities - ItemN /w dataType = "Group"
                        # parse "side" property too
                        if (len(class_path) == 3):

                            if (attr_name == 'dataType' and stripped_attr_value == 'Group'):

                                in_group_class = True

                            elif (attr_name == 'side' and (stripped_attr_value == 'West'
                                or stripped_attr_value == 'East' or stripped_attr_value == 'Independent')):

                                group_side = stripped_attr_value

                                if (not sides.get(group_side)):
                                    sides[group_side] = []

                                sides[group_side].append({'units': []})

                                #print 'new group', group_side

                            elif (attr_name == 'dataType' and stripped_attr_value == 'Object'):

                                in_object_class = True

                            elif (attr_name == 'dataType' and stripped_attr_value == 'Logic'):

                                in_logic_class = True


                            elif (is_vehicle_class and attr_name == 'type'):

                                vehicles[-1]['type'] = stripped_attr_value

                            #elif (attr_name == 'id' or attr_name == 'type'):
                            #    
                            #    print attr_name, stripped_semi_attr_value

                        elif (not in_unit_class and in_group_class and group_side):

                            #print class_path

                            #print line

                            # Mission → Entities → ItemN /w dataType == 'Group' → Entities → ItemN
                            if (len(class_path) == 5 and attr_name == 'dataType' and stripped_attr_value == 'Object'):

                                # add empty unit dict to the last group units list
                                #print sides[group_side][-1]

                                sides[group_side][-1]['units'].append({})

                                #print sides[group_side][-1], '---'

                                in_unit_class = True

                            # Mission → Entities → ItemN /w dataType == 'Group' → CustomAttributes
                            #    → AttributeN /w property == "groupID" - Value - data - 'value' property
                            elif (len(class_path) == 5 and class_path[3] == 'CustomAttributes'
                                and attr_name == 'property' and stripped_attr_value == 'groupID'):

                                #print 2323, in_unit_class, line

                                in_group_custom_attr_group_id = True

                            # Mission - Entities - ItemN /w dataType = "Group" - CustomAttributes -
                            #   AttributeN /w property == "groupID" - Value - data - 'value' property
                            elif (in_group_custom_attr_group_id and len(class_path) == 7 and attr_name == 'value'):

                                #print 'l\n', line, '\nl'

                                sides[group_side][-1]['groupID'] = stripped_attr_value
                        
                        elif (in_unit_class):

                            # parse "side" property too. just in case

                            if (attr_name == 'init' or attr_name == 'description' or attr_name == 'type'):

                                #print stripped_attr_value

                                sides[group_side][-1]['units'][-1][attr_name] = stripped_attr_value
                            
                            if (attr_name == 'id'):

                                #print stripped_semi_attr_value

                                sides[group_side][-1]['units'][-1][attr_name] = stripped_semi_attr_value
                            
                            # isPlayable propert present only if slot is playable 
                            elif (attr_name == 'isPlayable' and stripped_semi_attr_value == '1'):

                                sides[group_side][-1]['units'][-1][attr_name] = True

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
                                
                                sides[group_side][-1]['units'][-1]['ace_isMedic'] = stripped_semi_attr_value

                            elif (in_unit_custom_attrs_engineer and len(class_path) == 9 and class_path[7] == 'Value'
                                and class_path[8] == 'data'):

                                #print 'ace_isEngineer', stripped_semi_attr_value

                                sides[group_side][-1]['units'][-1]['ace_isEngineer'] = stripped_semi_attr_value

                            #print class_path
                            #print line

                        elif (in_object_class):

                            #print class_path

                            #print line

                            if (len(class_path) == 4 and class_path[3] == 'Attributes'):
                                
                                if (attr_name == 'lock' and stripped_attr_value == 'UNLOCKED'):

                                    vehicles.append({})

                                    #print vehicles

                                    is_vehicle_class = True

                                elif (is_vehicle_class and attr_name == 'init'):
                                    
                                    #print line

                                    vehicles[-1]['init'] = stripped_attr_value

                        elif (in_logic_class):

                            #print class_path

                            #print line

                            # CustomAttributes - AttributeN
                            if (len(class_path) == 5 and class_path[3] == 'CustomAttributes' and
                                attr_name == 'property'):
                                
                                if (stripped_attr_value == 'WMT_Main_DisableFuelSt'):
                                
                                    in_logic_class_custom_attr_disable_fuel_st = True

                                elif (stripped_attr_value == 'WMT_Main_AutoMedicine'):
                                
                                    in_logic_class_custom_attr_auto_med_provision = True

                                elif (stripped_attr_value == 'WMT_Main_SideChannelByLR'):
                                
                                    in_logic_class_custom_attr_side_channel_by_lr = True

                            elif (in_logic_class_custom_attr_disable_fuel_st and attr_name == 'value' and
                                stripped_semi_attr_value == '0'):
                                
                                wmt_disable_fuel_stations = False

                            elif (in_logic_class_custom_attr_auto_med_provision and attr_name == 'value' and
                                stripped_semi_attr_value == '0'):
                                
                                wmt_auto_med_provision = False

                            elif (in_logic_class_custom_attr_side_channel_by_lr and attr_name == 'value' and
                                stripped_semi_attr_value == '0'):
                                
                                wmt_side_channel_by_lr = False


    if (wmt_disable_fuel_stations):
    
        print 'WMT: Fuel stations are disabled'

    else:

        print 'WMT: Fuel stations are enabled'


    if (wmt_auto_med_provision):
    
        print 'WMT: Auto medicine provision is disabled'

    else:

        print 'WMT: Auto medicine provision is enabled'


    if (wmt_side_channel_by_lr):
    
        print 'WMT: Side channel by LR is enabled'

    else:

        print 'WMT: Side channel by LR is disabled'


    # 0 if found, 1 if not and 2 if error
    wog3_no_auto_long_range_radio = True if not call(
        [
            'grep',
            #'-i',
            '-o',
            # stop after first match
            #'-m', '1',
            'wog3_no_auto_long_range_radio = true;',
            path_to_mission_folder + '/init.sqf'
        ],
        stdout=devnull,
        stderr=devnull
    ) else False


    groupLeadersUniqueInits = set()

    if (wog3_no_auto_long_range_radio):
        
        print 'Has set no auto long range radio'

    else:
        
        # Check equpment of first units in squads (team leaders) for backpacks
        # If unit has backpack, then radio will be spawned behind him
        for side in sides:
            
            for group in sides[side]:

                print side, group.get('groupID') or 'group without groupID', group['units'][0]

                init = group['units'][0].get('init')

                if (init):
                    
                    groupLeadersUniqueInits.add(init)

                else:
                    
                    print '^^^ has no init'

        for init in groupLeadersUniqueInits:
            
            print init

            # 0 if found, 1 if not and 2 if error
            print 'has backpack, will dup' if not call(
                [
                    'grep',
                    '-i',
                    '-o',
                    # stop after first match
                    '-m', '1',
                    #'^_this addBackpack',
                    'addBackpack',
                    path_to_mission_folder + '/' + '/'.join(
                        init.split('""')[1].split('\\')
                    )
                ],
                stdout=devnull,
                stderr=devnull
            ) else ''


    print '\n~~~~\n'

    print '\nvehicles: %s' % (vehicles)

    for vehicle in vehicles:
        
        init = vehicle.get('init')
        
        if init:

            parse_results = parse_vehicle_init(init)

            if parse_results:

                print vehicle, parse_vehicle_init(init)


    total_playable_slots = 0

    playable_slots = {}

    uniqueUnitInits = set()

    # посчитать количество игровых слотов
    for side, groups in sides.items():
        
        if (not playable_slots.get(side)):

            playable_slots[side] = 0

        for group in groups:

            for unit in group['units']:

                uniqueUnitInits.add(unit.get('init'))

                if (unit.get('isPlayable')):

                    playable_slots[side] += 1

                    total_playable_slots += 1

    print '\nPlayable slots in total:', total_playable_slots

    if (total_playable_slots > 190):
        
        print '\nThe number of slots on missions should not exceed 190.'


    sorted_inits = sorted(uniqueUnitInits)

    print '\n\n'
    print sorted_inits

    unique_sorted_inits = []
    
    for init in sorted_inits:

        # None if no init
        if (init):
            
            print 'init:', init
            splitted_init = init.split('""')

            if (len(splitted_init) > 1):

                unique_sorted_inits.append([
                    init,
                    splitted_init[1],
                    # 0 if found, 1 if not and 2 if error
                    '' if not call(
                        [
                            'grep',
                            '-i',
                            '-o',
                            # stop after first match
                            #'-m', '1',
                            'itemradio',
                            path_to_mission_folder + '/' + '/'.join(
                                splitted_init[1].split('\\')
                            )
                        ],
                        stdout=devnull,
                        stderr=devnull
                    ) else 'Has no radio',
                    checkVanillaEquip(init)
                ])

            else:

                unique_sorted_inits.append([init])

    devnull.close()


    print '\nUnique unit inits:\n%s' % (
        '\n'.join(
            map(
                lambda x: ' — '.join(x),
                unique_sorted_inits
            )
        )
    )


    for side, groups in sides.items():
        
        print '\n', side, 'has', playable_slots[side], 'playable slots'

        for group in groups:

            print '\nGROUP ID:', group.get('groupID') or 'group without groupID'

            for unit in group['units']:

                if (unit.get('isPlayable')):

                    print '\n', unit['description'], unit['type'],  customAttrIsEngineer(unit.get('ace_isEngineer')),\
                        customAttrIsMedic(unit.get('ace_isMedic'))

                    print unit.get('init')

                else:
                    
                    print 'next unit is not playable!', unit
