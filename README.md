how to run project 

python -m venv venv

& .\venv\Scripts\Activate.ps1

python --version


pip install django
pip freeze > requirements.txt




python manage.py makemigrations
python manage.py migrate


python manage.py createsuperuser



Username: admin
Email: admin@example.com
Password: ********

python manage.py runserver


