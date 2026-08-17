import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

password = quote_plus(os.getenv("DB_PASSWORD"))

database_url = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{password}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(database_url)

with engine.connect() as connection:
    result = connection.execute(text("SELECT PostGIS_Version();"))
    print("PostGIS version:", result.scalar())