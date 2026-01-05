import os
import json
from restaurant_agent import suggest_restaurants


def main():


    api_key = os.getenv("GOOGLE_API_KEY")
    print("GOOGLE_API_KEY loaded:", api_key is not None)

    result = suggest_restaurants("Stockholm")
    import json
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))



if __name__ == "__main__":
    main()
