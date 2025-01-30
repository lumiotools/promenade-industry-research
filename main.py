from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
load_dotenv()
from services.overview import OverviewService
from services.industry_kpi import IndustryKpiService
from services.challenges import ChallengesService
from services.market import MarketService
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    MarketService.get_paragraph()
    