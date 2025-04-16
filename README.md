## Environment Variables
### 1. `.env` File
This file contains configuration for the Backend service, Celery, Redis, and Database connections.

#### Example `.env` File:
```ini
  SECRET_KEY=
  DEBUG=
  ALLOWED_HOSTS=
  DATABASE_NAME=
  DATABASE_USER=
  DATABASE_PASS=
  DATABASE_HOST=
  DATABASE_PORT=
  REDIS_HOST=
  REDIS_PORT=
  REDIS_DB=
  CELERY_BROKER_URL=
  CELERY_RESULT_BACKEND=
```

## How to run the app: 
1. Clone the repository:
 ```sh
 $ git clone https://github.com/MahshadAzizi/ubaar_auth.git
 $ cd ubaar_auth
 ```
2. Run Locally:
```sh
$ python manage.py migrate
$ python manage.py runserver
```
3. Run Celery:
```sh
$ celery -A config worker --loglevel=info 
```
