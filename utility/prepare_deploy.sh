#!/bin/bash

while (( "$#" )); do
    if [ "$1" == "--bc211Path" ]
    then
        BC211Path=$2
        shift 2
    elif [ "$1" == "--newComersGuidePath" ]
    then
        NewcomersGuidePath=$2
        shift 2
    elif [ "$1" == "--recommendationsToAddPath" ]
    then
        ManualRecommendations=$2
        shift 2
    elif [ "$1" == "--topicsToRemovePath" ]
    then
        TopicsToRemove=$2
        shift 2
    elif [ "$1" == "--servicesToRemovePath" ]
    then
        ServicesToRemove=$2
        shift 2
    elif [ "$1" == "--outputDir" ]
    then
        CurrentDate=`date '+%Y'-'%m'-'%d'`
        OutputFile=$2/data-$CurrentDate.json
        shift 2
    else
        echo "$1: Invalid command argument"
        usage
        exit
    fi
done

usage() {
    echo
    echo "Usage:"
    echo
    echo "    $0 [arguments]"
    echo
    echo "Mandatory arguments:"
    echo
    echo "    --bc211Path"
    echo "                The path to the BC211 data set in XML iCarol format."
    echo
    echo "    --newComersGuidePath"
    echo "                The path to the Newcomers' guide content."
    echo
    echo "    --recommendationsToAddPath"
    echo "                The path to the file containing manual recommendations."
    echo
    echo "    --topicsToRemovePath"
    echo "                The path to a file containing zero or more ids of topics for which"
    echo "                there should be no services recommended."
    echo
    echo "    --servicesToRemovePath"
    echo "                The path to a file containing zero or more ids of services that should"
    echo "                not be recommended for any topic."
    echo
    echo "    --outputDir"
    echo "                The directory where the output json file will be placed."
    echo
}

validateFilePath () {
    if [ "$1" == "" ]; then
        echo "Missing a required argument: $2"
        usage
        exit
    fi
    if [ ! -f "$1" ]; then
        echo "$1: file does not exist"
        usage
        exit
    fi
}

validateNewcomersGuidePath () {
    if [ "$NewcomersGuidePath" == "" ]; then
        echo "Missing required argument: Newcomers Guide path"
        usage
        exit
    fi
    if [ ! -d $NewcomersGuidePath ]; then
        echo "$NewcomersGuidePath: directory does not exist"
        usage
        exit
    fi
}

validateOutputFile () {
    if [ "$OutputFile" == "" ]; then
        echo "Missing a required argument for output"
        usage
        exit
    fi
    if [ -f $OutputFile ]; then
        echo "$OutputFile: Output file already exists"
        exit
    fi
}


validateFilePath "$BC211Path" "BC 211 data"

validateNewcomersGuidePath

validateFilePath "$ManualRecommendations" "Recommendations to add"
validateFilePath "$TopicsToRemove" "Topics to remove"
validateFilePath "$ServicesToRemove" "Services to remove"

validateOutputFile

echo "About to reinitialize database with data from:"
echo "BC211 data at:             $BC211Path"
echo "Newcomers data at:         $NewcomersGuidePath"
echo "Manual recommendations:    $ManualRecommendations"
echo "Topics to not recommend:   $TopicsToRemove"
echo "Services to not recommend: $ServicesToRemove"
echo "Output file:               $OutputFile"
read -p "Enter to continue, Ctrl-C to abort "

checkForSuccess () {
    if [ "$?" != "0" ]
    then
        echo "failed to $1"
        exit
    fi
}

echo "updating BC211 version string in bc211/__init.py__"
echo "__bc211_version__ = '$CurrentDate'" > ./bc211/__init__.py

./manage.py reset_db
checkForSuccess "reset database"

./manage.py migrate
checkForSuccess "migrate database"

echo "importing BC-211 data ..."
./manage.py import_bc211_data $BC211Path
checkForSuccess "import BC211 data"

./manage.py import_newcomers_guide --save_topics_to_db $NewcomersGuidePath
checkForSuccess "create newcomers guide fixtures"

echo "computing similarity scores ..."
./manage.py compute_text_similarity_scores --related_topics 3 --related_services 100 $NewcomersGuidePath
checkForSuccess "compute similarity scores"

echo "removing similarity scores for certain topics ..."
./manage.py remove_recommendations_for_topics $TopicsToRemove
checkForSuccess "remove similarity scores for topics"

echo "removing similarity scores for certain services ..."
./manage.py remove_recommendations_for_services $ServicesToRemove
checkForSuccess "remove similarity scores for services"

echo "adding manual similarity scores ..."
./manage.py set_manual_similarity_scores $ManualRecommendations
checkForSuccess "add manual similarity scores"

./manage.py dumpdata --natural-foreign --exclude auth.permission --exclude contenttypes --indent 4 > $OutputFile

checkForSuccess "dump data"
