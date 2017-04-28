# Flask example

Using Flask to build a Restful API Server with Swagger document.

Integration with Flask-restplus, Flask-Cors, Flask-Testing, Flask-SQLalchemy,and Flask-OAuth extensions.

### Extension:
- Restful: [Flask-restplus](http://flask-restplus.readthedocs.io/en/stable/)

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

- Testing: [Flask-Testing](http://flask.pocoo.org/docs/0.12/testing/)

- OAuth: [Flask-OAuth](https://pythonhosted.org/Flask-OAuth/)

- ESDAO: [elasticsearch](https://elasticsearch-py.readthedocs.io/en/master/) , [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)


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
| | |────user/
| | |────oauth/
| |──────config.Development.cfg
| |──────config.Production.cfg
| |──────config.Testing.cfg
| |────dao/
| |────model/
| |────oauth/
| |────util/
|──────run.py
|──────tests/

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


### OAuth Setup
add your `client_id` and `client_secret` into config file.

### ESDAO Setup
add your `ES host` and `ES port` into config file 



 
## Run Flask
### Run flask for develop
```
$ python webapp/run.py
```
In flask, Default port is `5000`

Swagger document page:  `http://127.0.0.1:5000/api`

### Run flask for production

** Run with gunicorn **

In  webapp/

```
$ gunicorn -w 4 -b 127.0.0.1:5000 run:app

```

* -w : number of worker
* -b : Socket to bind


### Run with Docker

```
$ docker build -t flask-example .

$ docker run -p 5000:5000 --name flask-example flask-example 
 
```

In image building, the webapp folder will also add into the image


## Unittest
```
$ nosetests webapp/ --with-cov --cover-html --cover-package=app
```
- --with-cov : test with coverage
- --cover-html: coverage report in html format

## Reference

Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [Flask restplus](http://flask-restplus.readthedocs.io/en/stable/)
- [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [Flask-OAuth](https://pythonhosted.org/Flask-OAuth/)
- [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)
- [gunicorn](http://gunicorn.org/)

Tutorial

- [Flask Overview](https://www.slideshare.net/maxcnunes1/flask-python-16299282)
- [In Flask we trust](http://igordavydenko.com/talks/ua-pycon-2012.pdf)

[Wiki Page](https://github.com/tsungtwu/flask-example/wiki)



## Changelog

- Version 2.3 : add dockerfile
- Version 2.2 : add ESDAO module
- Version 2.1 : add OAuth extension: FLASK-OAuth, and google oauth example
- Version 2.0 : add SQL ORM extension: FLASK-SQLAlchemy
- Version 1.1 : update nosetest
- Version 1.0 : basic flask-example with Flask-Restplus, Flask-Tesintg