# Fast Api PostGres BoilerPlate

## Getting Started

1. Install dependencies

```zsh
pip install -r requirements.txt
```

2. Start FastAPI process

```zsh
fastapi dev app/main.py
```

3. Open local API docs [http://localhost:5000/docs](http://localhost:5000/docs)

4. Sample docker env file

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
