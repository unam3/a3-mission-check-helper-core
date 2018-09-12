#!/usr/bin/env bash

# to test script run:
#. ~/a3/check.sh

#rm -rf ~/a3/wog_156_voshod_10.Takistan.pbo/ && . ~/a3/check.sh ~/a3/wog_156_voshod_10.Takistan.pbo

# $1 is first argument to this script as in example above

function check_pbo {
    #/home/yay/a3/wog_156_voshod_10.Takistan.pbo
    #echo $1

    filename=`sed -n -E 's/^(.*\/)*//p' <<< $1`

    #echo $filename

    filename_check=`sed -n -E '/^wog_[0-9]{2,3}_[a-z0-9_]+_[0-9]{2}\.[A-Za-z0-9_]+\.pbo$/p' <<< $filename`

    if [[ -z $filename_check ]];
        then echo "wrong mission file name: $filename";

        return;
    fi

    extractpbo_msg_last_line=`extractpbo $1 |& tail -n 1` 
    
    if [[ $extractpbo_msg_last_line != "No Error(s)" ]];
        then {
            echo $extractpbo_msg_last_line;

            return;
        }
    fi
    
    # get the folder name from .pbo filename
    mission_folder=`sed s/\.pbo$// <<< $1`;

    #echo $mission_folder;

    mission_sqm=$mission_folder/mission.sqm;

    # check if mission.sqm was binarize
    # get the second line and search RE in it
    mission_was_deraped=`head -n 2 $mission_sqm | grep "^//DeRap: wog_"`;

    if [[ -z $mission_was_deraped ]];
        then {
            echo "mission.sqm wasn't binarized.";
            
            return;
        }
    fi
    
    python2 mission_check.py $mission_sqm;
}

function run_tests {
    echo 'starting tests'

    # "to_test
    test_filenames=(
        "pluh"
        "Takistan.pbo"
        "og_156_voshod.10.Takistan.pbo"
        "og_156_voshod_10.Tak.istan.pbo"
        "og_6_voshod_10.Tak.istan.pbo"
        "og_156_voshod_10.Takistan.pbo"
    )

    i=0;

    while [[ -n ${test_filenames[i]} ]]
    do {
        test_results=`check_pbo ${test_filenames[i]};`

        test_failed_result="wrong mission file name: ${test_filenames[i]}"

        #echo $test_results
        #echo $test_failed_result

        if [ test_results == test_failed_result ]
        then
            echo 'test' $i $test_failed_result
        fi

        i=$(($i+1))
    } done
}

# if first param is not set
if [[ -z $1 ]];
    then run_tests;
    else check_pbo $1;
fi

# TODO: check size of the images
# filesize in KB
#ls -kl loadscreen.jpg |cut -d ' ' -f 5
