#!/bin/bash

# to test script run:
#. ~/a3/check.sh

#rm -rf ~/a3/wog_54_retranslyator_14.Sara_dbe1 && . ~/a3/check.sh ~/a3/wog_54_retranslyator_14.Sara_dbe1.pbo
#rm -rf ~/a3/wog_100_nastuplenie_10.ruha && . ~/a3/check.sh ~/a3/wog_100_nastuplenie_10.ruha.pbo
#rm -rf ~/a3/wog_89_the_boar_that_stuck_10.fallujah && . ~/a3/check.sh ~/a3/wog_89_the_boar_that_stuck_10.fallujah.pbo
#rm -rf ~/a3/wog_135_after_party_10.FDF_Isle1_a && . ~/a3/check.sh ~/a3/wog_135_after_party_10.FDF_Isle1_a.pbo
#rm -rf ~/a3/wog_135_after_party_10.FDF_Isle1_a && . ~/a3/check.sh ~/a3/wog_135_after_party_10.FDF_Isle1_a.pbo > log
#rm -rf ~/a3/wog_123_ada_12.pja307 && . ~/a3/check.sh ~/a3/wog_123_ada_12.pja307.pbo > log
#rm -rf ~/a3/wog_88_welcome_to_the_jungle_10.lingor3 && . ~/a3/check.sh ~/a3/wog_88_welcome_to_the_jungle_10.lingor3.pbo > log
#rm -rf ~/a3/wog_48_tymanoe_ytro_10.chernarus_summer && . ~/a3/check.sh ~/a3/wog_48_tymanoe_ytro_10.chernarus_summer.pbo > log
#rm -rf ~/a3/wog_133_sistema_pro_10.ruha && . ~/a3/check.sh ~/a3/wog_133_sistema_pro_10.ruha.pbo > log

# $1 is first argument to this script as in example above

function check_pbo {
    #/home/yay/a3/wog_156_voshod_10.Takistan.pbo
    #echo $1

    #filename check was here

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
    
    # for working pipes
    PYTHONIOENCODING=UTF-8 python2 mission_check.py $mission_folder;


    description_file_path=$mission_folder/Description.ext;

    if [[ -a $description_file_path ]];
        then {
            echo "mission has Description.ext!";
        }
    fi    
}

# if first param is not set
#if [[ -z $1 ]];
#    then run_tests;
#    else check_pbo $1;
#fi

check_pbo $1;

# TODO: check size of the images
# filesize in KB
#ls -kl loadscreen.jpg |cut -d ' ' -f 5
