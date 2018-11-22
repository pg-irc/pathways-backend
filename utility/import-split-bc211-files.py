import os
from subprocess import call

for file in os.listdir('./data'):
    call(['./manage.py', 'import_bc211_data', './data/' + file])
