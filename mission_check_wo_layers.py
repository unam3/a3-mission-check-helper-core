#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re, sys, os, json, exceptions

from vehicles_n_boxes import box, air, land_vehicle, ship

from subprocess import call, check_output, CalledProcessError


class CustomError(exceptions.Exception):

    def __init__(self, value):

        self.value = value

    def __str__(self):

        return repr(self.value)

class CheckVanillaEquipError(CustomError): pass

class GetMissionFilesListError(CustomError): pass


def getMissionFilesList(path, devnull):

    out = None

    try:
        out = check_output(
            [
                'find',
                path,
                # list only files
                '-type', 'f'
            ],
            stderr=devnull
        )

    except CalledProcessError as shi:

        print shi

        raise GetMissionFilesListError(('eeeh?', path))

    return None if (not out) else map(
        lambda fullpath: fullpath.split(path + '/')[1],
        out.decode('utf-8', 'replace').splitlines()
    )


def get_wog3_no_auto_long_range_radio(path_to_init_sqf, devnull):

    # 0 if found, 1 if not and 2 if error
    return True if not call(
        [
            'grep',
            #'-i',
            '-o',
            # stop after first match
            #'-m', '1',
            'wog3_no_auto_long_range_radio = true;',
            path_to_init_sqf
        ],
        stdout=devnull,
        stderr=devnull
    ) else False


def has_backpack_in_init(path_to_init, devnull, backpacks_to_find):

    # 0 if found, 1 if not and 2 if error
    return not call(
        [
            'grep',
            '-i',
            '-o',
            # stop after first match
            '-m', '1',
            backpacks_to_find,
            path_to_init
        ],
        stdout=devnull,
        stderr=devnull
    )


# https://github.com/michail-nikolaev/task-force-arma-3-radio/blob/master/arma3/%40task_force_radio/addons/task_force_radio_items/config.cpp
# grep ItemRadio
personal_radios = 'itemradio\\|tf_anprc152\\|tf_anprc148jem\\|tf_fadak\\|tf_anprc154\\|tf_rf7800str\\|tf_pnr1000a'

#copytoclipboard str ("((configName _x) isKindOf 'Backpacks') && (getNumber (_x >> 'tf_hasLRradio') != 0) && (getNumber (_x >> 'scope') >= 2)" configClasses (configFile >> "CfgVehicles") apply {
#    [
#        configName _x
#    ]
#});

# TFAR_Bag_Base for the reason that some give itemRadio and some may give it? Check this out
#'TFAR_Bag_Base\\\\|' + .map(([className]) => className).join('\\\\|')
backpack_radios = 'TFAR_Bag_Base\\|usm_pack_alice_prc119\\|usm_pack_alice_prc77\\|usm_pack_st138_prc77\\|tf_rt1523g\\|tf_rt1523g_bwmod\\|tf_rt1523g_rhs\\|tf_rt1523g_big\\|tf_rt1523g_big_bwmod\\|tf_rt1523g_big_bwmod_tropen\\|tf_rt1523g_big_rhs\\|tf_rt1523g_sage\\|tf_rt1523g_green\\|tf_rt1523g_fabric\\|tf_rt1523g_black\\|tf_anprc155\\|tf_anprc155_coyote\\|tf_mr3000\\|tf_mr3000_multicam\\|tf_mr3000_bwmod\\|tf_mr3000_bwmod_tropen\\|tf_mr3000_rhs\\|tf_bussole\\|tf_anarc210\\|tf_anarc164\\|tf_mr6000l\\|UK3CB_BAF_B_Bergen_MTP_Radio_H_A\\|UK3CB_BAF_B_Bergen_MTP_Radio_H_B\\|UK3CB_BAF_B_Bergen_MTP_Radio_L_A\\|UK3CB_BAF_B_Bergen_MTP_Radio_L_B\\|UK3CB_BAF_B_Bergen_MTP_JTAC_H_A\\|UK3CB_BAF_B_Bergen_MTP_JTAC_L_A\\|UK3CB_BAF_B_Bergen_MTP_SL_H_A\\|UK3CB_BAF_B_Bergen_MTP_SL_L_A\\|UK3CB_BAF_B_Bergen_DDPM_SL_A\\|UK3CB_BAF_B_Bergen_DDPM_JTAC_A\\|UK3CB_BAF_B_Bergen_DDPM_JTAC_H_A\\|UK3CB_BAF_B_Bergen_DPMW_SL_A\\|UK3CB_BAF_B_Bergen_DPMW_JTAC_A\\|UK3CB_BAF_B_Bergen_DPMW_JTAC_H_A\\|UK3CB_BAF_B_Bergen_DPMT_SL_A\\|UK3CB_BAF_B_Bergen_DPMT_JTAC_A\\|UK3CB_BAF_B_Bergen_DPMT_JTAC_H_A\\|UK3CB_BAF_B_Bergen_Arctic_SL_A\\|UK3CB_BAF_B_Bergen_Arctic_JTAC_A\\|UK3CB_BAF_B_Bergen_Arctic_JTAC_H_A\\|UK3CB_BAF_B_Bergen_OLI_SL_A\\|UK3CB_BAF_B_Bergen_OLI_JTAC_A\\|UK3CB_BAF_B_Bergen_OLI_JTAC_H_A\\|UK3CB_BAF_B_Bergen_TAN_SL_A\\|UK3CB_BAF_B_Bergen_TAN_JTAC_A\\|UK3CB_BAF_B_Bergen_TAN_JTAC_H_A'

def has_personal_radio_in_init(path_to_init, devnull):
    return bool(call(
        [
            'grep',
            '-i',
            '-o',
            # stop after first match
            #'-m', '1',
            personal_radios,
            path_to_init
        ],
        stdout=devnull,
        stderr=devnull
    ))


#def parse_vehicle_init(init):
#
#    setVariables = init.split('this setVariable [""')
#
#    init_options = {}
#    
#    # has any setVariable declaration
#    if len(setVariables) > 1:
#
#        for declaration in setVariables[1:]:
#
#            if declaration.startswith('tf_side'):
#
#                # tf_side"",""east""]; 
#                #print declaration
#                #print declaration[10:].split('""')[1]
#
#                init_options['tf_side'] = declaration[10:].split('""')[1]
#
#            elif declaration.startswith('WMT_Side'):
#
#                #print 'WMT_Side'
#                #print declaration
#                #print declaration[11:].strip(' ').split(']')[0]
#
#                init_options['WMT_Side'] = declaration[11:].strip(' ').split(']')[0]
#
#    return init_options if len(init_options) else None


def checkVanillaEquip(init_path, current_script_dir, devnull):

    #print init_path

    out = None

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

        # shi.returncode == 1 — grep was not found any matching substring in file
        # if 2 — no such file as init_path
        if (shi.returncode != 1):

            raise CheckVanillaEquipError(('no_such_init_file', init))

    return '' if (not out) else out.decode('utf-8')


def check(path_to_mission_folder):

    #print 'check', path_to_mission_folder

    check_results = {
        'mission_attrs': {},
        'slots': {},
        'errors': {},
        'warnings': {}
    }

    path_to_mission_sqm = path_to_mission_folder + '/mission.sqm'

    devnull = open(os.devnull, 'w')

    current_script_dir = os.path.dirname(os.path.abspath(__file__))


    missionFilesListLowercaseMapping = {}

    for path_to_file in getMissionFilesList(path_to_mission_folder, devnull):

        missionFilesListLowercaseMapping[path_to_file.lower()] = path_to_file

    #print missionFilesListLowercaseMapping


    wmt_disable_fuel_stations = True

    wmt_auto_med_provision = True

    wmt_side_channel_by_lr = True


    with open(path_to_mission_sqm) as opened_mission_file:
        #print opened_mission_file

        sides = {}

        vehicles = []

        boxes = []

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

        object_class_custom_attr = False

        object_class_attrs = {}

        in_logic_class = False

        in_logic_class_custom_attr_disable_fuel_st = False

        in_logic_class_custom_attr_auto_med_provision = False

        in_logic_class_custom_attr_side_channel_by_lr = False

        for line in opened_mission_file:
        #for number, line in enumerate(opened_mission_file):

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

                elif (in_object_class):

                    if len(class_path) == 3:

                        in_object_class = False

                        object_class_attrs = {}

                    elif (object_class_custom_attr and len(class_path) == 5):

                        #print 'term', len(class_path), class_path

                        #print line

                        object_class_custom_attr = False

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


                # TODO: for testing purposes
                #print number, class_path
                #class_path.pop()

                if len(class_path) > 0:
                    
                    class_path.pop()

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

                            check_results['mission_attrs']['author'] = stripped_attr_value

                        if (attr_name == 'loadScreen'):

                            check_results['mission_attrs']['loadScreen'] = stripped_attr_value

                        if (attr_name == 'saving' and stripped_semi_attr_value != '0'):
                            
                            check_results['mission_attrs']['w_saving'] = True

                        if (attr_name == 'respawn' and stripped_semi_attr_value != '1'):
                            
                            check_results['mission_attrs']['w_respawn'] = True

                    elif (class_path[0] == str('CustomAttributes')):

                        #general attr
                        if ((len(class_path) == 6 and class_path[1] == 'Category0' and class_path[2] == 'Attribute0'
                            and class_path[3] == 'Value' and class_path[4] == 'data' and class_path[5] == 'value' 
                            and attr_name == 'items' and stripped_semi_attr_value != str(1))
                            or (len(class_path) == 8 and class_path[1] == 'Category0' and class_path[2] == 'Attribute0'
                            and class_path[3] == 'Value' and class_path[4] == 'data' and class_path[5] == 'value'
                            and class_path[6] == 'Item0' and class_path[7] == 'data'
                            and attr_name == 'value' and stripped_attr_value != 'Spectator')):

                                check_results['mission_attrs']['w_respawn_rulesets'] = True

                        #general attrs
                        if (len(class_path) == 3 and class_path[1] == 'Category1' and class_path[2] == 'Attribute0'
                            and attr_name == 'property' and stripped_attr_value != 'EnableTargetDebug'):

                                check_results['mission_attrs']['w_enable_target_debugging'] = True

                    elif (class_path[0] == str('Mission')):

                        if (class_name == 'Intel'):
                            #print splitted_attribute_definition
                            
                            if (attr_name == 'briefingName'):

                                check_results['mission_attrs']['briefing_name'] = stripped_attr_value

                                if (not re.match('WOG \d{2,3} (\w+\ )+\d\.\d$', stripped_attr_value, re.UNICODE)):

                                    check_results['mission_attrs']['wrong_briefing_name'] = True

                            # side (color, attack) - side (color, def)
                            elif (attr_name == 'overviewText'):

                                #print stripped_attr_value.encode('utf-8')
                                
                                check_results['mission_attrs']['overview_text'] = stripped_attr_value

                            elif ((attr_name == 'startWind' or attr_name == 'forecastWind')
                                and float(stripped_semi_attr_value) >= 0.41):

                                check_results['mission_attrs']['w_wind'] = int(float(stripped_semi_attr_value) * 100)

                            elif ((attr_name == 'startRain' or attr_name == 'forecastRain')
                                and float(stripped_semi_attr_value) >= 0.41):

                               check_results['mission_attrs']['w_rain'] = int(float(stripped_semi_attr_value) * 100)

                        elif (len(class_path) >= 2 and class_path[1] == str('Entities')):

                            #print in_object_class, line

                            # Mission - Entities - ItemN /w dataType = "Group"
                            # parse "side" property too
                            if (len(class_path) == 3):

                                if (attr_name == 'dataType' and stripped_attr_value == 'Group'):

                                    in_group_class = True

                                elif (in_group_class and attr_name == 'side' and (stripped_attr_value == 'West'
                                    or stripped_attr_value == 'East' or stripped_attr_value == 'Independent')):

                                    group_side = stripped_attr_value

                                    if (not sides.get(group_side)):
                                        sides[group_side] = []

                                    #print len(sides[group_side]), class_path

                                    sides[group_side].append({'units': []})

                                    #print 'new group', group_side

                                elif (attr_name == 'dataType' and stripped_attr_value == 'Object'):

                                    in_object_class = True

                                elif (attr_name == 'dataType' and stripped_attr_value == 'Logic'):

                                    in_logic_class = True

                                elif (in_object_class):

                                    #print class_path

                                    #print line

                                    if attr_name == 'type':
                                        
                                        vehicle_name = (
                                            air.get(stripped_attr_value) or
                                            land_vehicle.get(stripped_attr_value)
                                            or ship.get(stripped_attr_value)
                                        )

                                        if vehicle_name:

                                            object_class_attrs['type'] = stripped_attr_value

                                            object_class_attrs['name'] = vehicle_name

                                            vehicles.append(object_class_attrs)

                                        else:

                                            box_name = box.get(stripped_attr_value)

                                            if box_name:

                                                object_class_attrs['type'] = stripped_attr_value

                                                object_class_attrs['name'] = box_name

                                                boxes.append(object_class_attrs)
                                        

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
                                
                                elif (attr_name == 'id'):

                                    #print stripped_semi_attr_value

                                    sides[group_side][-1]['units'][-1][attr_name] = stripped_semi_attr_value
                                
                                elif ((attr_name == 'isPlayable' or attr_name == 'isPlayer')
                                    and stripped_semi_attr_value == '1'):

                                    sides[group_side][-1]['units'][-1]['isPlayable'] = True

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

                                elif (in_unit_custom_attrs_engineer and len(class_path) == 9
                                    and class_path[7] == 'Value' and class_path[8] == 'data'):

                                    #print 'ace_isEngineer', stripped_semi_attr_value

                                    sides[group_side][-1]['units'][-1]['ace_isEngineer'] = stripped_semi_attr_value

                                elif (len(class_path) == 7 and class_path[5] == 'Attributes'
                                    and class_path[6] == 'Inventory'):
                                    
                                    sides[group_side][-1]['units'][-1]['has_inventory'] = True

                                    check_results['warnings']['has_unit_with_inventory'] = True

                                #print class_path
                                #print line

                            elif (in_object_class):

                                #print class_path

                                #print line

                                if (len(class_path) == 4 and class_path[3] == 'Attributes'):
                                    
                                    if (attr_name == 'lock' or attr_name == 'init' or attr_name == 'description'):

                                        object_class_attrs[attr_name] = stripped_attr_value

                                    elif (attr_name == 'health' or attr_name == 'ammo' or attr_name == 'fuel'):

                                        object_class_attrs[attr_name] = int(float(stripped_semi_attr_value) * 100)

                                #[u'Mission', u'Entities', u'Item3', u'CustomAttributes', u'Attribute0']
                                #property = "ace_isMedicalVehicle";


                                elif (len(class_path) == 5 and class_path[3] == 'CustomAttributes'):
                                    

                                    if (attr_name == 'property' and
                                        (stripped_attr_value == 'ace_isMedicalVehicle' or
                                        stripped_attr_value == 'ace_isRepairVehicle')
                                    ):

                                        #print stripped_attr_value

                                        object_class_custom_attr = stripped_attr_value

                                #[u'Mission', u'Entities', u'Item3', u'CustomAttributes', u'Attribute1', u'Value', u'data']
                                #value = 1.0;

                                elif (object_class_custom_attr and len(class_path) == 7 and
                                    class_path[5] == 'Value' and class_path[6] == 'data'):

                                        #print 'object_class_custom_attr', class_path

                                        #print line

                                        vehicles[-1][object_class_custom_attr] = stripped_semi_attr_value

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


        check_results['mission_attrs']['wmt_disable_fuel_stations'] = wmt_disable_fuel_stations

        check_results['mission_attrs']['wmt_auto_med_provision'] = wmt_auto_med_provision

        check_results['mission_attrs']['wmt_side_channel_by_lr'] = wmt_side_channel_by_lr


        wog3_no_auto_long_range_radio = False

        init_sqf = missionFilesListLowercaseMapping.get('init.sqf')

        if init_sqf:

            path_to_init_sqf = path_to_mission_folder + '/' + init_sqf

            wog3_no_auto_long_range_radio = get_wog3_no_auto_long_range_radio(path_to_init_sqf, devnull)

            if (wog3_no_auto_long_range_radio):
                
                check_results['mission_attrs']['wog3_no_auto_long_range_radio'] = True


        # get slots count, uniq inits
        playable_slots = {}

        uniqueUnitInits = set()

        groupLeadersUniqueInits = set()

        for side, groups in sides.items():
            
            if (not playable_slots.get(side)):

                playable_slots[side] = 0

            for group in groups:

                for i, unit in enumerate(group['units']):

                    init = unit.get('init')

                    # in case of use predefined structures (wog/rhs)
                    if (init):

                        uniqueUnitInits.add(init)

                        if i == 0:

                            groupLeadersUniqueInits.add(init)

                    if (unit.get('isPlayable')):

                        playable_slots[side] += 1

        check_results['slots']['playable_slots'] = playable_slots


        #clientside this!
        #if (total_playable_slots > 190):
        #    
        #    check_results['slots']['too_much_slots'] = True


        sorted_uniq_inits = sorted(uniqueUnitInits)

        #print sorted_uniq_inits

        unique_inits_attrs = []
        
        for init in sorted_uniq_inits:
            
            unique_init_attrs = {'init': init}

            # None if no init
            if (init):

                #print 'init:', init
                
                # proper init example:
                # call{this call compile preprocessfilelinenumbers ""equipment_infanterie\Russian_army\msv\spn_sniper.sqf"";}
                
                # unsupported (Crabe-) init example:
                # call{[this, ""BAND"", ""LEAD""] call compile preprocessFileLineNumbers ""process_units.sqf"";}

                if not re.search('this call compile preprocessfilelinenumber', init, re.UNICODE|re.IGNORECASE):

                    unique_init_attrs['unsupported_equipment_init'] = True

                else:

                    splitted_init = init.split('""')

                    if (len(splitted_init) > 1):

                        unique_init_attrs['splitted_init'] = splitted_init[1]

                        lowercase_init = missionFilesListLowercaseMapping.get(
                           '/'.join(
                                splitted_init[1].split('\\')
                            ).lower()
                        )

                        if bool(lowercase_init):
                        
                            path_to_init = path_to_mission_folder + '/' + lowercase_init

                            if init in groupLeadersUniqueInits:

                                #'^_this addBackpack',
                                backpacks_to_find = 'addBackpack' if not wog3_no_auto_long_range_radio else backpack_radios

                                if has_backpack_in_init(path_to_init, devnull, backpacks_to_find):

                                    # If unit has backpack, then radio will be spawned behind him
                                    if not wog3_no_auto_long_range_radio:

                                        unique_init_attrs['backpack_will_dup'] = True

                                        check_results['errors']['has_unit_with_backpack_dup'] = True

                                elif wog3_no_auto_long_range_radio:

                                    unique_init_attrs['group_leader_without_lrr'] = True

                                    check_results['warnings']['has_group_leader_without_lrr'] = True


                            if has_personal_radio_in_init(path_to_init, devnull):
                                
                                unique_init_attrs['has_no_radio'] = True

                                check_results['warnings']['has_unit_without_personal_radio'] = True


                            try:

                                vanilla_equipment = checkVanillaEquip(path_to_init, current_script_dir, devnull)

                            except CheckVanillaEquipError as shi:

                                vanilla_equipment = ''

                                (error, path) = shi.value

                                print error, path

                                if (not check_results['errors'].get(error)):

                                    check_results['errors'][error] = []

                                #'return code: %s for %s' % (shi.returncode, init_path)
                                check_results['errors'][error].append(path)


                            if len(vanilla_equipment):

                                unique_init_attrs['vanilla_equipment'] = vanilla_equipment

            unique_inits_attrs.append(unique_init_attrs)

        devnull.close()

        check_results['slots']['unique_inits'] = unique_inits_attrs

        check_results['sides'] = sides

        check_results['vehicles'] = vehicles

        #filters boxes without an init (some may be placed as decorations)
        check_results['boxes'] = filter(
            lambda bdict: bdict.get('init'),
            boxes
        )


        if missionFilesListLowercaseMapping.get('description.ext'):

            check_results['warnings']['has_description_ext'] = True
            

        # TODO: check size of the images
        # filesize in KB
        #ls -kl loadscreen.jpg |cut -d ' ' -f 5

        return check_results


if __name__ == "__main__":
    
    # this and singlequotes in templates around output wasn't good enough
    #print json.dumps(check_results, ensure_ascii=False)
    print json.dumps(json.dumps(check(sys.argv[1]), ensure_ascii=False), ensure_ascii=False)
