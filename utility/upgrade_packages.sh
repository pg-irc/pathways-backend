#!/bin/bash

ENVIRONMENT='venv-upgrade'

if [[ $1 = 'local' ]]
then
    REQUIREMENTS='requirements/local.txt'
    CONFIG='config.settings.local'
fi

echo "Interactive upgrade of packages in $REQUIREMENTS"
#echo "*********************************************************************"
pur -r $REQUIREMENTS -i

echo "Installing upgraded requirements from $REQUIREMENTS in $ENVIRONMENT"
rm -rf $ENVIRONMENT
python3 -m venv $ENVIRONMENT
source $ENVIRONMENT/bin/activate
pip install -r $REQUIREMENTS
export DJANGO_SETTINGS_MODULE=$CONFIG
python manage.py test

# echo 'Please source venv-upgrade/bin/activate and test manually and check in changes if all looks good'
