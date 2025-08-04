python3 -m venv venv
source venv/bin/activate  

pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver


https://dbdiagram.io/d/mediphore-6887dc92cca18e685c1fe1d2

# mediphore
A system that matches project tasks to resources based on required skills and availability. It includes a matching algorithm, REST APIs, database design, and sample data for validation. Delivers sequence diagram, schema, and a working Django-based backend for task-resource allocation.
