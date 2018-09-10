#!/usr/bin/env bash

# to test script run:
#rm -rf ~/a3/c/ && . ~/a3/check.sh ~/a3/c.pbo

# $1 is first argument to this script as in example above

#echo $1

extractpbo_msg_last_line=`extractpbo $1 |& tail -n 1` 

if [[ $extractpbo_msg_last_line != "No Error(s)" ]];
    then echo $extractpbo_msg_last_line;

    else {
        # get the folder name from .pbo filename
        mission_folder=`sed s/\.pbo$// <<< $1`;

        echo $mission_folder;

        # check if mission.sqm was binarize
        #head -n 2 ~/a3/wog_96_the_forgotten_war_latest.lingor3/mission.sqm | grep "^//DeRap: wog_"
    }
fi


#python2 mission_check.py

# filesize in KB
#ls -kl loadscreen.jpg |cut -d ' ' -f 5
