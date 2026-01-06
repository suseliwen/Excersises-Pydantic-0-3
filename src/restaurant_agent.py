import os
from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError
from models import Restaurant, RestaurantSuggestions
from dotenv import load_dotenv

load_dotenv()

def env_flag(name: str, default: bool = False) -> bool:             #Hjälpfunktion för att aktivera/deaktivera mockdata för att spara credits
    value = os.getenv(name, str(default)).strip().lower()
    return value in ("1", "true", "yes", "y", "on")

USE_MOCK = env_flag("USE_MOCK", default=False)    
print("USE_MOCK resolved to:", USE_MOCK)
              

agent = Agent(
    model="google-gla:gemini-2.5-flash-lite",
    output_type = RestaurantSuggestions,
    system_prompt=(
        "You suggest restaurants near a given location. "
        "Return exactly 5 restaurants."
    ),
)

def _mock_five(location: str) -> RestaurantSuggestions:
    restaurants = [
        Restaurant(
            name=f"Mock Place {i}",
            cuisine="Italian",
            price_level="$$",
            rating=4.2,
            description="Fallback restaurant (no API quota).",
            opening_hours="Mon-Fri 11-22",
            location=location,
        )
        for i in range(1, 6)
    ]
    return RestaurantSuggestions(location=location, restaurants=restaurants)


def suggest_restaurants(location: str) -> RestaurantSuggestions:

    if USE_MOCK:
        return _mock_five(location)
    
    else:
        try:
            result = agent.run_sync(f"Location: {location}")
            return result.output
        
        except ModelHTTPError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print("Hit Google quota/rate limit -> using mock fallback.")
                return _mock_five(location)
            raise

    
 
