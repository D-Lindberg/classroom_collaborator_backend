import sys, os
import shutil

root = os.path.dirname(os.path.abspath(__file__))
def removeMigrationFiles():
    fNames = os.listdir(os.path.join(root, 'Classroom/migrations'))
    for fName in fNames:
        path = os.path.join(root, 'Classroom/migrations', fName)
        if not fName.endswith('__init__.py'):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

def refreshDatabase():
    os.system('dropdb ClassDB')
    os.system('createdb ClassDB')

def migrateDatabase():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classroom_collaborator_backend.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])


if __name__ == "__main__":
    removeMigrationFiles()
    refreshDatabase()
    migrateDatabase()