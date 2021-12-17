# Server of the Goren PnP

## Virtual Env
- create  `python3 -m venv ./venv`
- enter   `./venv/Scripts/activate`
- leave   `deactivate`


## Dependencies for Django Backend (outdated)

Update via `pip freeze > .\requirements.txt`

```python
Django==3.*							# need django for django. Makes sense, right?

#Twisted==20.3.0                 # set specific version to use in uvicorn (asgi-server)
#uvicorn[standard]               # asgi server, need async for websockets in chat (does not exist in alpine version of docker-image)
#gunicorn>=20.0.4				# prod env for django

Twisted[tls,http2]==21.*        # needed for HTTP/2 support of daphne
daphne==3.*                     # prod env for (sync django &) async django channels (via ws)

Pillow>=8								# image library
psycopg2-binary>=2.8.6					# for postgresql usage
pytz>=2018.4						# better handling for time/date types
django-request>=1.5.5		# http-request logging in /admin/request/...
django-dbbackup==3.*        # db + media backup utility

channels==3.*

six==1.* # generate token for email confirmation on signup

djangorestframework==3.*    # rest-framework
djangorestframework-simplejwt==5.*    # rest-framework jwt
pyyaml==6.*     # generate rest-schema
uritemplate==4.*
coreapi==2.*    # visualize schema -> ui
```
