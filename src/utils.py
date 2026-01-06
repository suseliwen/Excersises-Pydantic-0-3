from pathlib import Path
import duckdb
import uuid
from datetime import datetime, timezone
from src.models import Restaurant


DATA_PATH = Path(__file__).parent / "data"
DB_PATH = DATA_PATH / "restaurants.duckdb"


def execute_duckdb(sql_code: str, parameters = None) -> None:
    """ Kör SQL som inte ska returnera data (CREATE/INSERT/UPDATE/DELETE)"""
    DATA_PATH.mkdir(exist_ok = True)
    with duckdb.connect(DB_PATH) as conn:
        conn.execute(sql_code, parameters)


def select_duckdb(sql_code: str, parameters = None):
    """Kör SELECT och returnerar en Data Frame"""
    DATA_PATH.mkdir(exist_ok= True)
    with duckdb.connect(DB_PATH) as conn:
        cursor = conn.execute(sql_code, parameters)
        return cursor.df()
    

def insert_restaurant(
        *,
        input_location: str,
        input_cuisine: str,
        restaurant: Restaurant,
) -> None:
    sql = """

        INSERT INTO restaurants (
            id,
            created,
            input_location,
            input_cuisine,
            name,
            cuisine,
            price_level,
            rating,
            description,
            opening_hours,
            location
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    parameters = (
        str(uuid.uuid4()),
        datetime.now(timezone.utc),
        input_location,
        input_cuisine,
        restaurant.name,
        restaurant.cuisine,
        restaurant.price_level,
        restaurant.rating,
        restaurant.description,
        restaurant.opening_hours,
        restaurant.location,
    )

    execute_duckdb(sql, parameters)

    def select_duckdb(sql_code: str, parameters = None) -> list[dict]:
        """ Kör SELECT och returnerar en lista[dict]."""
        df = select_duckdb(sql_code, parameters)
        return df.to_dict(orient = "records")