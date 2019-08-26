. env/bin/activate

hg update

pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --noinput

python manage_sou.py migrate
python manage_sou.py collectstatic --noinput
