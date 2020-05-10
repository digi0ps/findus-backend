cd /code;
echo "Migrating";
python manage.py migrate --no-input;
echo "Moving static files";
python manage.py collectstatic --noinput;
echo "Starting gunicorn";
gunicorn --bind :8000 --workers=4 root.wsgi:application;