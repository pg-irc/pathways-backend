#!/bin/bash

ENVIRONMENT='venv-upgrade'

main() {
    handle_command_line_argument $1
    upgrade_requirement_files
    install_packages_in_clean_environment
    run_tests
    print_summary_message_to_standard_out
}

handle_command_line_argument() {
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
}

upgrade_requirement_files() {
    print_message "Interactive upgrade of packages in $REQUIREMENTS"
    pur -r $REQUIREMENTS -i
}

print_message() {
    echo
    echo $1
    echo
}

install_packages_in_clean_environment()
{
    print_message "Installing requirements from $REQUIREMENTS in clean environment $ENVIRONMENT"
    rm -rf $ENVIRONMENT
    python3 -m venv $ENVIRONMENT
    source $ENVIRONMENT/bin/activate
    pip install -r $REQUIREMENTS
}

run_tests() {
    export DJANGO_SETTINGS_MODULE=$CONFIG
    python manage.py test
}

print_summary_message_to_standard_out() {
    echo
    echo "Execute"
    echo
    echo "   source $ENVIRONMENT/bin/activate"
    echo "   export DJANGO_SETTINGS_MODULE=$CONFIG"
    echo
    echo "and perform whatever manual testing is needed"
    echo "before checking in changes in requirements/"
    echo
}

main $1
