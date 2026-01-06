import os
import json
from src.restaurant_agent import suggest_restaurants
from dotenv import load_dotenv


def main():

    load_dotenv()
    print("USE_MOCK:", os.getenv("USE_MOCK"))

    api_key = os.getenv("GOOGLE_API_KEY")
    print("GOOGLE_API_KEY loaded:", api_key is not None)

    result = suggest_restaurants("Göteborg")
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))



if __name__ == "__main__":
    main()
