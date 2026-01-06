from src.models import Restaurant
from src.utils import insert_restaurant, select_duckdb

r = Restaurant(
    name="Test Bistro",
    cuisine="French",
    price_level="$$",
    rating=4.3,
    description="Inserted from test script",
    opening_hours="11-22",
    location="Göteborg",
)

insert_restaurant(
        input_location="Göteborg",
        input_cuisine="French",
        restaurant=r,
)

print(select_duckdb("SELECT * FROM restaurants"))