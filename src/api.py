from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.utils import execute_duckdb, select_duckdb
from src.models import RestaurantCreateRequest


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # säkrar att tabellen finns när API:t startar
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
    yield


@app.get("/restaurants")
def get_restaurants():
    return select_duckdb("SELECT * FROM restaurants ORDER BY created DESC;")

@app.post("/restaurants")
async def create_restaurant(body: RestaurantCreateRequest):
    return {
        "received_location": body.location,
        "received_cuisine": body.cuisine,
    }
