from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from openai import OpenAI
import json
import subprocess
import re
import os
from fastapi.responses import FileResponse

# Initialize FastAPI app
app = FastAPI(
    title="Industry Analysis API",
    description="Simple API for generating industry analysis presentations",
    version="1.0.0"
)

# Initialize OpenAI client
client = OpenAI()

# Pydantic model for request validation
class PresentationRequest(BaseModel):
    industry: str

# Import services
from Overview import OverviewService
from Distribution import DistributionService
from Regulation import RegulationService
from Trends import TrendsService
from IndustryEvolution import IndustryEvolutionService
from ValueChain import ValueChainService
from CompetitiveLandscape import CompetitiveLandscapeService
from Challenges import ChallengesService
from Market import MarketService
from IndustryKpi import IndustryKpiService

class GlossaryService:
    @staticmethod
    def extract_terms(content: str) -> list:
        """Extract technical terms from content."""
        terms = set()
        
        # Find terms in bold
        bold_terms = re.findall(r'\*\*(.*?)\*\*', content)
        terms.update(bold_terms)
        
        # Find terms in code blocks
        code_terms = re.findall(r'`(.*?)`', content)
        terms.update(code_terms)
        
        # Find capitalized technical terms
        cap_terms = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', content)
        terms.update(cap_terms)
        
        return sorted(list(terms))

    @staticmethod
    def generate_glossary(terms: list) -> str:
        """Generate glossary content using OpenAI."""
        try:
            system_prompt = """
            You are a technical glossary generator. Create definitions for the provided technical terms.
            Format the output as a markdown glossary organized alphabetically.
            """
            
            user_prompt = f"""
            Create a glossary for these technical terms: {', '.join(terms)}
            Format as:
            # Glossary

            **A**
            * **Term1**: Definition
            * **Term2**: Definition

            Only include letters that have associated terms.
            Organize terms alphabetically under their respective letters.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating glossary: {str(e)}")

class PresentationService:
    @staticmethod
    def create_markdown(slides: list, industry: str, include_glossary: bool = True) -> str:
        """Create markdown content for the presentation."""
        try:
            markdown_content = """---
marp: true
paginate: true
---

<style>
section {
    font-size: 16px;
    padding: 20px;
}
h1 {
    font-size: 24px;
    margin-bottom: 16px;
}
table {
    font-size: 14px;
    width: 100%;
}
</style>

"""
            # Add title slide
            markdown_content += f"# {industry.title()} Industry Analysis\n\n---\n\n"
            
            # Add content slides
            for slide in slides:
                markdown_content += f"{slide}\n\n---\n\n"
            
            # Generate and add glossary if requested
            if include_glossary:
                terms = GlossaryService.extract_terms(markdown_content)
                if terms:
                    glossary_content = GlossaryService.generate_glossary(terms)
                    markdown_content += f"{glossary_content}\n\n---\n\n"
            
            return markdown_content
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating markdown: {str(e)}")

    @staticmethod
    def generate_presentation(industry: str) -> List[str]:
        """Generate all presentation slides."""
        try:
            slides = []
            
            # Generate content from all services
            overview_data = OverviewService.get_paragraph(industry)
            market_data = MarketService.get_paragraph(industry)
            evolution_data = IndustryEvolutionService.get_evolution_content(industry)
            competitive_data = CompetitiveLandscapeService.get_slides(industry)
            value_chain_data = ValueChainService.get_paragraph(industry)
            distribution_data = DistributionService.get_paragraph(industry)
            challenges_data = ChallengesService.get_paragraph(industry)
            kpi_data = IndustryKpiService.generate_tabular(industry)
            regulation_data = RegulationService.get_paragraph(industry)
            trends_data = TrendsService.get_paragraph(industry)
            
            # Add slides in order
            slides.extend([
                overview_data["overview_slide_1_overview_paragraph"],
                overview_data["overview_slide_2_sector_wise_key_activities_table"],
                overview_data["overview_slide_3_use_cases_table"],
                market_data["market_slide_1_overview_paragraph"],
                market_data["market_slide_2_sector_wise_key_activities_table"],
                market_data["market_slide_3_major_segment"],
                market_data["market_slide_4_market_segment_table"],
                market_data["market_slide_5_application_table"],
                market_data["market_slide_6_end_users_table"],
                market_data["market_slide_7_core_technology"],
                f"# Industry Evolution\n\n{evolution_data['industry_evolution_slide_1_evolution_overview']}\n\n{evolution_data['industry_evolution_slide_2_timeline']}",
                evolution_data["industry_evolution_slide_3_future_trends"],
                competitive_data["competitive_landscape_slide_1_overview"],
                competitive_data["competitive_landscape_slide_2_factors"],
                f"# Value Chain\n\n{value_chain_data}",
                distribution_data["distribution_slide_1_end_customers"],
                distribution_data["distribution_slide_2_distribution_models_and_partners"],
                distribution_data["distribution_slide_3_emerging_channels"],
                challenges_data["challenges_slide_1_challenges_and_opportunities_paragraph"],
                kpi_data["industry_kpi_slide_1_industry_kpi_table"],
                regulation_data["regulation_silde_1_regulatory_bodies"],
                regulation_data["regulation_silde_2_key_regulations"],
                regulation_data["regulation_silde_3_licensing_requirements"],
                trends_data["trends_slide_1_recent_trends"],
                trends_data["trends_slide_2_expansion_services"],
                trends_data["trends_slide_3_industry_categories"]
            ])
            
            return slides
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating presentation: {str(e)}")

@app.post("/generate-presentation")
async def generate_presentation(request: PresentationRequest):
    """
    Generate a complete industry analysis presentation with glossary.
    Returns the PowerPoint file for download.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Generate presentation slides
        slides = PresentationService.generate_presentation(request.industry)
        
        # Create markdown with glossary
        markdown_content = PresentationService.create_markdown(slides, request.industry)
        
        # Save markdown file
        markdown_path = f"output/{request.industry}_presentation.md"
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        # Generate PowerPoint using Marp
        pptx_path = f"output/{request.industry}_presentation.pptx"
        command = f"marp --pptx {markdown_path} -o {pptx_path}"
        subprocess.run(command, shell=True)
        
        # Return PowerPoint file
        if os.path.exists(pptx_path):
            return FileResponse(
                pptx_path,
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                filename=f"{request.industry}_presentation.pptx"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate PowerPoint file")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Startup event to create output directory
@app.on_event("startup")
async def startup_event():
    os.makedirs("output", exist_ok=True)

# Shutdown event to clean up files
@app.on_event("shutdown")
async def shutdown_event():
    if os.path.exists("output"):
        for file in os.listdir("output"):
            file_path = os.path.join("output", file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)