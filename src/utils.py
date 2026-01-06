from pathlib import Path
import duckdb


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