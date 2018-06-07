# D&D 5e spell database

This flask app uses [wkhtmltopdf](https://wkhtmltopdf.org/),            [SQLAlchemy](http://www.sqlalchemy.org/), [wtforms](https://github.com/wtforms/wtforms), [pdfkit](https://pypi.org/project/pdfkit/) and a [SQLite](https://www.sqlite.org/index.html) Database to generate printable pdf files of spells filtered by the user.

## Instalation

CD into the FLASK folder
```sh
$ cd FLASK
```
You should use the included venv, use the following command to activate it and set the FLASK local variables:

### Mac:
```sh
$ source venv/Scripts/activate
$ export FLASK_APP=app.py
```

### Windows:
```sh
$ venv\Scripts\activate.bat
$ SET FLASK_APP=app.py
```

Now start serving the app in debug mode, if you want to deactivate debug mode change the last line in 'FLASK/app.py' and remove the 'debug=True':
```sh
$ flask run
```


## Requirements
All requiremnts are available with pip:
```sh
$ pip install [module]
```
Note that you should install the modules for python3 and plain pip may be linked to python2, in that case use:
```sh
$ python3 -m pip install [module]
```
You may also need to use 'sudo'
#### [Flask](http://flask.pocoo.org/), [SQLAlchemy](http://www.sqlalchemy.org/), [wtforms](https://github.com/wtforms/wtforms), [pdfkit](https://pypi.org/project/pdfkit/)



License
----

Copyright (c) 2018 Rubin Raithel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

