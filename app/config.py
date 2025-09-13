from dotenv import load_dotenv
import os

# explicitly load .env.local
load_dotenv(".env.local")

# environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
