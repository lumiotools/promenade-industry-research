from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
load_dotenv()
from services.Overview import OverviewService
from services.Distribution import DistributionService
from services.Regulation import RegulationService
from services.Trends import TrendsService
from services.IndustryEvolution import IndustryEvolutionService
from services.ValueChain import ValueChainService 
from services.CompetitiveLandscape import CompetitiveLandscapeService
from services.Challenges import ChallengesService
from services.Market import MarketService
from services.IndustryKpi import IndustryKpiService

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # OverviewService.get_paragraph()
    # MarketService.get_paragraph()
    # IndustryEvolutionService.get_evolution_content()
    # CompetitiveLandscapeService.get_slides()
    # IndustryEvolutionService.get_evolution_content()
    # ValueChainService.get_paragraph()
    # DistributionService.get_paragraph()
    # ChallengesService.get_paragraph()
    IndustryKpiService.generate_tabular()
    # RegulationService.get_paragraph()
    # TrendsService.get_paragraph()
