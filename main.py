from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# API Endpoint to provide data to your frontend
@app.get("/api/financial-summary")
async def get_summary():
    return {
        "net_worth": "₹1,24,50,000",
        "monthly_income": "₹8,50,000",
        "health_score": 88
    }

# Serve the static frontend files
# 'html=True' ensures index.html is served at the root URL
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # This runs your server at http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
