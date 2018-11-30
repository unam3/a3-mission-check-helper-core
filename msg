#print 'Author:', stripped_attr_value
check_results['mission_attrs']['author'] = stripped_attr_value

#print 'Load screen image:', stripped_attr_value
check_results['mission_attrs']['loadScreen'] = stripped_attr_value

#print 'Сохранение должно быть выключено.'.encode('utf-8')
check_results['mission_attrs']['w_saving'] = True

#print 'Respawn must be set to "Spectator".'
check_results['mission_attrs']['w_respawn'] = True

#print 'Only "Spectator" option must be set in the "Rulesets" of the "Multiplayer" attributes'
check_results['mission_attrs']['w_respawn_rulesets'] = True

#print 'Please turn on "Enable Target Debugging"'
check_results['mission_attrs']['w_enable_target_debugging'] = True

#print 'Mission name:', attr_value
check_results['mission_attrs']['w_enable_target_debugging'] = attr_value

#print 'Название миссии не удовлетворяет шаблону.'.encode('utf-8')
check_results['mission_attrs']['w_briefing_name'] = True

#print stripped_attr_value.encode('utf-8')
check_results['mission_attrs']['overview_text'] = stripped_attr_value.encode('utf-8')

#print 'Wind must be less than or equal to 40%:', int(float(stripped_semi_attr_value) * 100)
check_results['mission_attrs']['w_wind'] = int(float(stripped_semi_attr_value) * 100)

#print 'Rain must be less than or equal to 40%:', int(float(stripped_semi_attr_value) * 100)
check_results['mission_attrs']['w_rain'] = int(float(stripped_semi_attr_value) * 100)

#print 'WMT: Fuel stations are disabled'
check_results['mission_attrs']['wmt_disable_fuel_stations'] = True
else         print 'WMT: Fuel stations are enabled'


if (wmt_auto_med_provision):
print 'WMT: Auto medicine provision is enabled'

check_results['mission_attrs']['wmt_side_channel_by_lr'] = True
print 'WMT: Side channel by LR is enabled'

check_results['mission_attrs']['wog3_no_auto_long_range_radio'] = True
print 'Has set no auto long range radio'

check_results['slots']['total_count'] = total_playable_slots
print '\nPlayable slots in total:', total_playable_slots

check_results['slots']['total_count'] = total_playable_slots
print '\nThe number of slots on missions should not exceed 190.'

check_results['warnings']['backpacks_dup'] = init
print 'has backpack, will dup'
