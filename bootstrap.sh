sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo su postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'postgres'\" "
sudo su postgres -c "createdb -E UTF8 -T template0 --locale=en_US.utf8 -O postgres bank"
sudo apt-get install -y python3
sudo apt-get install -y python-pip
sudo apt-get install -y python-virtualenv
virtualenv -p python3 bank
source bank/bin/activate
cd /vagrant
pip install -r requirements/test.txt
python manage.py migrate --settings=config.settings.test

