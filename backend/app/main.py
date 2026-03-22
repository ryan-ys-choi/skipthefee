from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_connection
from app.ai import estimate_prices


app = FastAPI(title="SkipTheFee API")

# Allow React frontend to access to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    ai_results = estimate_prices(restaurant, city)
    for r in ai_results:
        r["restaurant"] = restaurant
        r["city"] = city
        r["estimated"] = True
    return {"results": ai_results, "source": "ai"}