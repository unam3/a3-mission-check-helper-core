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
        briefing_name: 'Название миссии не удовлетворяет шаблону.',

        saving: 'Сохранение должно быть выключено.',

        respawn: 'Respawn must be set to "Spectator".',

        respawn_rulesets: 'Only "Spectator" option must be set in the "Rulesets" of the "Multiplayer" attributes.',

        enable_target_debugging: 'Please turn on "Enable Target Debugging".',

        wind: 'Wind must be less than or equal to 40%:',

        rain: 'Rain must be less than or equal to 40%:',

        backpacks_dup: 'has backpack, will dup',

        has_no_radio: 'has no radio', 
    },
    errors: {
        vanilla_equipment: 'Has forbidden vanilla equipment:',
        mission_wasnt_binarized: 'mission.sqm wasn\'t binarized!',
        wrong_filename: 'Incorrect filename!',
        extraction_error: 'Extraction error!',
        unsupported_equipment_init: "Unsupported equipment init"
    }
};
