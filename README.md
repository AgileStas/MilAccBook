1. Setup environment

```bash
git clone git@github.com:AgileStas/MilAccBook.git # https://github.com/AgileStas/MilAccBook.git
python -m venv MilAccBook
cd MilAccBook
. bin/activate
cd MilLog
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py makemigrations MilAccBook
./manage.py migrate
# if you have initial data, put it into ./MilAccBook/fixtures/
[ -d MilAccBook/fixtures ] && for fname in MilAccBook/fixtures/*.json; do ./manage.py loaddata `basename $fname .json`; done
```

2. Test environment

```bash
# in the same virtual environment, same directory
./manage.py runserver
```

Visit [products page](http://127.0.0.1:8000/book/product/) in your environment.
