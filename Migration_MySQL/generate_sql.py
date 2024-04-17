import os 

import sys 
from django.core.management import execute_from_command_line
sys.path.append('/Users/sk_courseworks/Course_Work/cs673/PROJECT_PHASE2/SimplyWealth/SimplyWealthProject')
os.chdir('/Users/sk_courseworks/Course_Work/cs673/PROJECT_PHASE2/SimplyWealth/SimplyWealthProject')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SimplyWealthProject.settings')

execute_from_command_line(['manage.py', 'makemigrations'])
migration_dir= '/Users/sk_courseworks/Course_Work/cs673/PROJECT_PHASE2/SimplyWealth/SimplyWealthProject/SimplyWealthApp/migrations/'
migration_files = sorted(os.listdir(migration_dir))

with open('simplywealthDB_schema.sql', 'w') as f:
    for migration_file in migration_files:
        if migration_file.endswith('.py') and migration_file != '__init__.py':
            migration_name = migration_file.replace('.py', '')
            sql_output = os.popen(f'python manage.py sqlmigrate SimplyWealthApp {migration_name}').read()
            f.write(sql_output)
            f.write(';\n\n')
            breakpoint()

