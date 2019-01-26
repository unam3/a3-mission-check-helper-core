const msg = {
    mission_attrs: {
        author: 'Author:',
        loadScreen: 'Load screen image:',
        briefing_name: 'Mission name:',
        overview_text: 'Overview text:',
        //wog3_no_auto_long_range_radio: 'Has set no auto long range radio provision',
        wog3_no_auto_long_range_radio: 'Auto long range radio provision',
        //wmt_auto_med_provision: 'WMT: Auto medicine provision is enabled',
        wmt_auto_med_provision: 'WMT: Auto medicine provision',
        //wmt_side_channel_by_lr: 'WMT: Side channel only by long radio is enabled',
        wmt_side_channel_by_lr: 'WMT: Side channel only with long radio',
        //wmt_disable_fuel_stations: 'WMT: Fuel stations are disabled',
        wmt_disable_fuel_stations: 'WMT: Fuel stations can refuel',
    },
    slots: {
        squad_default_name: 'Aplha 1-',
    },
    warnings: {
        has_no_radio: 'has no radio', 
        has_unit_without_personal_radio: 'There is at least one unit without personal radio.',
    },
    errors: {
        mission_was_not_binarized: 'mission.sqm was not binarized!',
        wrong_filename: 'Incorrect filename!',
        extraction_error: 'Extraction error!',

        not_playable_unit: 'this unit is not playable!',
        unsupported_equipment_init: 'Unsupported equipment inits',
        unallowed_path_to_equipment_script: 'Unallowed path to equipment script. Only alphabetical, numerical characters, "\", "-", "." are ok.',
        no_such_init_file: 'There is no such file!',

        vanilla_equipment: 'Unit init has forbidden vanilla equipment',
        has_unit_with_backpack_dup: 'Has at least one squad with the squad leader (first unit) with duplicated backpack!',
        backpack_will_dup: 'backpack from the equipment will spawn behind squad leader\'s back with this init; LRR will be on unit',

        //wrong_briefing_name: 'Название миссии не удовлетворяет шаблону.',
        wrong_briefing_name: 'Mission name is incorrect.',
        //saving: 'Сохранение должно быть выключено.',
        saving: 'Saving must be disabled.',
        respawn: 'Respawn must be set to "Spectator".',
        respawn_rulesets: 'Only "Spectator" option must be set in the "Rulesets" of the "Multiplayer" attributes.',
        enable_target_debugging: 'Please turn on "Enable Target Debugging".',
        wind: 'Wind must be less than or equal to 40%:',
        rain: 'Rain must be less than or equal to 40%:',
    },
};
