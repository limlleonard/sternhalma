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