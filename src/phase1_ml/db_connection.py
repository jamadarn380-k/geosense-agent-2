import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()


def get_engine():
    """Create and return the PostgreSQL/PostGIS database engine."""

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "geosense_db")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise ValueError(
            "DB_PASSWORD was not found. Check the .env file in the GeoSense project folder."
        )

    connection_string = (
        f"postgresql://{user}:{password}@{host}:{port}/{database}"
    )

    return create_engine(connection_string)


def test_connection():
    """Test the PostgreSQL/PostGIS connection."""

    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT PostGIS_Version();"))
        version = result.fetchone()[0]

        print("Connected successfully!")
        print("PostGIS version:", version)


if __name__ == "__main__":
    test_connection()