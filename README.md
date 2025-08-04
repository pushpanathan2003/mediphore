python3 -m venv venv
source venv/bin/activate  

pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver


https://dbdiagram.io/d/mediphore-6887dc92cca18e685c1fe1d2