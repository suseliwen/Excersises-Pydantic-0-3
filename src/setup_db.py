from utils import execute_duckdb

execute_duckdb("""
    CREATE TABLE IF NOT EXISTS restaurants (
                id TEXT,
                created TIMESTAMP,

                input_location TEXT,
                input_cuisine TEXT,

               name TEXT,
               cuisine TEXT,
               price_level TEXT,
               rating DOUBLE,
               description TEXT,
               opening_hours TEXT,
               location TEXT
    );
""")


