# httpout-login
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=nggit_httpout-login&metric=coverage)](https://sonarcloud.io/summary/new_code?id=nggit_httpout-login)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nggit_httpout-login&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nggit_httpout-login)

httpout-login is basically an extension of [httpout-session](https://github.com/nggit/httpout-session).

You can use it just like httpout-session but with additional methods like `login()`, `logout()`, and `is_logged_in()`.

## Usage
```python
# __globals__.py
from httpout_login import Session


def __enter__(app):
    # this is a session middleware
    # that enables you to use request.ctx.session in routes
    Session(app, expires=86400)
```

## Installing
```
python3 -m pip install --upgrade httpout_login
```

## Testing
Just run `python3 -m tests`.

Or if you also want measurements with [coverage](https://coverage.readthedocs.io/):

```
coverage run -m tests
coverage combine
coverage report
coverage html # to generate html reports
```

## License
MIT License
