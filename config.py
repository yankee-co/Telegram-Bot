import os

# Database settings come from environment variables.
# Copy .env.example to .env, fill in your values and load them before running.
host = os.getenv("DB_HOST", "127.0.0.1")
user = os.getenv("DB_USER", "postgres")
password = os.environ["DB_PASSWORD"]
db_name = os.getenv("DB_NAME", "shop")
port = os.getenv("DB_PORT", "5432")
