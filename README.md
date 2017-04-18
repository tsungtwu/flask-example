# Flask example

Using Flask to build a Restful API Server with Swagger document.

Also with Flask-restplus, Flask-Cors, Flask-Testing extensions.


## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
.
|──────app/
| |────__init__.py
| |────api/
| | |────__init__.py
| | |────cve/
| | |────tweet/
| |──────config.Development.cfg
| |──────config.Production.cfg
| |──────config.Testing.cfg
| |────model/
| |────util/
|──────run.py
|──────tests/
| |──────test_cve.py
| |──────test_twitter.py
| |──────testData/

```


## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```
### Configuring From Files

#### Example Usage

```
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
```

#### cfg example

```

##Flask settings
DEBUG = True  # True/False
TESTING = False

##SWAGGER settings
SWAGGER_DOC_URL = '/api'

....


```

#### Builtin Configuration Values

SERVER_NAME: the name and port number of the server. 

JSON_SORT_KEYS : By default Flask will serialize JSON objects in a way that the keys are ordered.

- [reference¶](http://flask.pocoo.org/docs/0.12/config/)


## Run Flask
```
$ python flask-example/run.py
```
In flask, Default port is `5000`

Swagger document page:  `http://127.0.0.1:5000/api`

## Run unittest
```
$ nosetests flask-example/ --with-cov --cover-html --cover-package=app
```
- --with-cov : test with coverage
- --cover-html: coverage report in html format

## Reference

Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [Flask restplus](http://flask-restplus.readthedocs.io/en/stable/)

Tutorial

- [Flask Overview](https://www.slideshare.net/maxcnunes1/flask-python-16299282)
- [In Flask we trust](http://igordavydenko.com/talks/ua-pycon-2012.pdf)