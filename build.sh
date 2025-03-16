set -o errexit
pip install -r requirements.txt
cd front
npm install
npm run build
cd ..
mkdir -p templates
cp front/dist/index.html templates/index.html
python manage.py collectstatic --no-input
python manage.py migrate
# gunicorn --bind 0.0.0.0:8000 back.wsgi
# daphne -b 0.0.0.0 -p 8000 back.asgi:application
# uvicorn back.asgi:application --host 0.0.0.0 --port 8000