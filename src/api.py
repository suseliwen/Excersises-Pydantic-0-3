from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.utils import execute_duckdb, select_duckdb, insert_restaurant
from src.models import RestaurantCreateRequest
from src.restaurant_agent import generate_restaurant


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


@app.get("/restaurants")            #Är synk pga gör ett snabbt, blockerande DB-anrop
def get_restaurants():
    return select_duckdb("SELECT * FROM restaurants ORDER BY created DESC;")


@app.post("/restaurant")
async def create_restaurant(body: RestaurantCreateRequest):
    restaurant = await generate_restaurant(
        location = body.location,
        cuisine= body.cuisine,
    )
    insert_restaurant(
        input_location= body.location,
        input_cuisine= body.cuisine,
        restaurant=restaurant,
    )
    
    return restaurant

#@app.post("/restaurant")
#async def create_restaurant(body: RestaurantCreateRequest):         # Är ASYNC pga behöver vänta på svar från AI, och måste kunna pausa för att inte blocka servern
    #return {
        #"received_location": body.location,
        #"received_cuisine": body.cuisine,
    #}


