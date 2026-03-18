import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def estimate_prices(restaurant: str, city: str):
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""
                Estimate delivery prices for {restaurant} in {city} 
                across DoorDash, Uber Eats, and Grubhub.
                
                Based on typical markup patterns:
                - DoorDash is usually cheapest with widest selection
                - Uber Eats tends to have higher item markups
                - Grubhub falls in the middle
                - Item prices on apps are 20-40% higher than menu price
                - Delivery fees range $2.99-$4.99
                - Service fees range $1.50-$3.00
                
                Return ONLY a JSON array, no explanation, no markdown:
                [
                    {{"platform": "doordash", "item_name": "Popular Item", "item_price": 11.99, "delivery_fee": 3.99, "service_fee": 2.50, "total": 18.48}},
                    {{"platform": "grubhub", "item_name": "Popular Item", "item_price": 12.49, "delivery_fee": 3.49, "service_fee": 2.00, "total": 17.98}},
                    {{"platform": "ubereats", "item_name": "Popular Item", "item_price": 13.99, "delivery_fee": 2.99, "service_fee": 1.50, "total": 18.48}}
                ]
                """
            }
        ]
    )

    response_text = message.content[0].text
    return json.loads(response_text)