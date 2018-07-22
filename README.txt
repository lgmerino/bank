Django application to manage bank users. Every user has a first name, last name and IBAN account.


Installing for local development

Download the repository
Create a virtualenv for python 3.x
Go to the root directory of the project
Install requirements with pip: pip install -r requirements/local.txt
(Postgres is not needed. Local environment uses a sqlite3 database)
Run migrations: python manage.py migrate --settings=config.settings.local
Launch the development server: python manage.py runserver --settings=config.settings.local
Open a web browser and visit http://localhost:8000
You'll be redirected to the google login page.
You can create users. See all the users in the application and update/delete only the users you create.


Running a vagrant virtual machine for testing

We need to install vagrant and virtualbox
After that go to the root directory of the project and execute:
vagrant up  # this will install in the virtual machine all we need (python3, pip, postgres, virtualenv and requirements)
vagrant ssh
source bank/bin/activate
cd /vagrant
python manage.py test --settings=config.settings.test  # this runs the tests



