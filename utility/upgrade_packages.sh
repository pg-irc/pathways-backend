#!/bin/bash

ENVIRONMENT='venv-upgrade'

if [[ $1 = 'local' ]]
then
    REQUIREMENTS='requirements/local.txt'
    CONFIG='config.settings.local'

elif [[ $1 = 'test' ]]
then
    REQUIREMENTS='requirements/test.txt'
    CONFIG='config.settings.test'

elif [[ $1 = 'production' ]]
then
    REQUIREMENTS='requirements/production.txt'
    CONFIG='config.settings.production'

else
    echo "Specify local, test or production"
    exit
fi

echo "Interactive upgrade of packages in $REQUIREMENTS"
pur -r $REQUIREMENTS -i

echo "Installing requirements from $REQUIREMENTS in clean environment $ENVIRONMENT"
rm -rf $ENVIRONMENT
python3 -m venv $ENVIRONMENT
source $ENVIRONMENT/bin/activate
pip install -r $REQUIREMENTS
export DJANGO_SETTINGS_MODULE=$CONFIG
python manage.py test

echo "Execute"
echo "   source $ENVIRONMENT/bin/activate"
echo "   export DJANGO_SETTINGS_MODULE=$CONFIG"
echo "and then perform whatever manual testing is needed"
echo "before checking in changes in requirements/"
