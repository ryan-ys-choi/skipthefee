import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database="skipthefee",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )
