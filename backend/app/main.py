from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_connection
from app.ai import estimate_prices


app = FastAPI(title="SkipTheFee API")

# Allow React frontend to access to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "SkipTheFee API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/search")
def search(restaurant: str, city: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT
                    r.name,
                    r.city,
                    p.platform,
                    p.item_name,
                    p.item_price,
                    p.delivery_fee,
                    p.service_fee,
                    p.total
                   FROM restaurants r
                    JOIN prices p ON r.id = p.restaurant_id
                    WHERE LOWER(r.name) LIKE LOWER(%s)
                    AND LOWER(r.city) = LOWER(%s)
                    ORDER BY p.total ASC
                   """, (f"%{restaurant}%", city))
    
    rows = cursor.fetchall()
    cursor.close()
    
    results = []
    for row in rows:
        results.append({
            "restaurant": row[0],
            "city": row[1],
            "platform": row[2],
            "item_name": row[3],
            "item_price": float(row[4]),
            "delivery_fee": float(row[5]),
            "service_fee": float(row[6]),
            "total": float(row[7])
        })

    if len(results) == 0:
        # If no data in DB, call AI to estimate prices
        ai_results = estimate_prices(restaurant, city)
        for r in ai_results:
            r["restaurant"] = restaurant
            r["city"] = city
            r["estimated"] = True
        return {"results": ai_results, "source": "ai"}

    return {"results": results, "source": "database"}