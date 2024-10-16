# athena

Example of eventsourcing with FastAPI

## Getting Started

1. Install dependencies

```zsh
frontend: npm install
backend: pip install -r requirements.txt
```

2. Start FastAPI process

```zsh
frontend: npm run dev
backend: fastapi dev app/main.py
```

3. Open local API docs [http://localhost:5000/docs](http://localhost:5000/docs)

4. Open local Next server [http://localhost:3000/](http://localhost:3000/)

5. Sample docker env file

frontend:

```commandline
NEXT_PUBLIC_LOCAL_BASE_URL=https://ec2-3-234-10-151.compute-1.amazonaws.com
NEXT_PUBLIC_WEB_SOCKET_BASE_URL=wss://ec2-3-234-10-151.compute-1.amazonaws.com
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyDjRMq25hfcfyjAJ50TaQls8UaJXSqKUb0
```

backend:

```commandline
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB_NAME=grant_engine
MAX_CONNECTIONS_COUNT=10
MIN_CONNECTIONS_COUNT=3
DATABASE_SCHEME=postgresql+asyncpg
REDIS_URL=redis://localhost:6379
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379
JWT_SECRET_KEY=thisshouldbesupersecret
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=120
RESET_TOKEN_EXPIRE_MINUTES=10
TOKEN_ALGORITHM=HS256
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=test@test.com
EMAIL_PASSWORD=testing
```
