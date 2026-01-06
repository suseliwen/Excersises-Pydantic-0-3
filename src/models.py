from pydantic import BaseModel, Field
from typing import Annotated


class Restaurant(BaseModel):
    name: str = Field(..., description="Restaurant name")
    cuisine: str = Field(..., description="Type of food (cuisine)")
    price_level: str = Field(..., description="Price level, e.g. $, $$, $$$")
    rating: float = Field(..., ge=0, le=5, description="Rating 0-5")
    description: str = Field(..., description="Short description")
    opening_hours: str = Field(..., description="Opening hours")
    location: str = Field(..., description="Where it is located")



class RestaurantSuggestions(BaseModel):
    location: str
    restaurants: Annotated[list[Restaurant], Field(min_length=5, max_length=5)]


class RestaurantCreateRequest(BaseModel):
    location: str = Field(..., description= "Where ti search")
    cuisine: str = Field(..., description= "Type of food, e.g. Italian, French, Chineese")


if __name__ == "__main__":
    r = Restaurant(
        name="Test Bistro",
        cuisine="French",
        price_level="$$",
        rating=4.2,
        description="A cozy place with classic dishes.",
        opening_hours="Mon-Sun 11:00-22:00",
        location="Gamla Stan, Stockholm",
    )

    s = RestaurantSuggestions(location="Gamla Stan, Stockholm", restaurants=[r])
    print(s.model_dump())