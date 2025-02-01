from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor
import re
import os
from openai import OpenAI
import subprocess

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

            **B**
            * **Term1**: Definition
            * **Term2**: Definition

            **C**
            * **Term1**: Definition
            * **Term2**: Definition

            .
            .
            .

            **Z**
            * **Term1**: Definition
            * **Term2**: Definition

            Only include letters that have associated terms.
            Organize terms alphabetically under their respective letters, with each letter containing a maximum of 3-4 terms.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
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
    async def run_service(service_func, *args):
        """Run a service function in a thread pool."""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, service_func, *args)

    @staticmethod
    async def create_markdown(slides: list, industry: str, include_glossary: bool = True) -> str:
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
                    # Split glossary content into slides for each letter
                    glossary_lines = glossary_content.splitlines()
                    current_letter = ""
                    letter_slide_content = ""
                    letter_count = 0  # Count letters for the slide

                    for line in glossary_lines:
                        if line.startswith("**"):
                            if letter_count >= 3:  # If 3 letters are already added, create a new slide
                                markdown_content += f"# Glossary\n\n{letter_slide_content}\n\n---\n\n"
                                letter_slide_content = ""
                                letter_count = 0  # Reset letter count
                            current_letter = line[3]  # Get the letter
                            letter_slide_content += line + "\n"
                            letter_count += 1  # Increment letter count
                        else:
                            letter_slide_content += line + "\n"
                    
                    # Add the last letter slide if exists
                    if letter_slide_content:
                        markdown_content += f"# Glossary\n\n{letter_slide_content}\n\n---\n\n"
            
            return markdown_content
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating markdown: {str(e)}")

    @staticmethod
    async def generate_presentation(industry: str) -> list:
        """Generate all presentation slides in parallel."""
        try:
            # Create tasks for all services
            tasks = [
                PresentationService.run_service(OverviewService.get_paragraph, industry),
                PresentationService.run_service(MarketService.get_paragraph, industry),
                PresentationService.run_service(IndustryEvolutionService.get_evolution_content, industry),
                PresentationService.run_service(CompetitiveLandscapeService.get_slides, industry),
                PresentationService.run_service(ValueChainService.get_paragraph, industry),
                PresentationService.run_service(DistributionService.get_paragraph, industry),
                PresentationService.run_service(ChallengesService.get_paragraph, industry),
                PresentationService.run_service(IndustryKpiService.generate_tabular, industry),
                PresentationService.run_service(RegulationService.get_paragraph, industry),
                PresentationService.run_service(TrendsService.get_paragraph, industry)
            ]

            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks)
            
            # Unpack results
            [overview_data, market_data, evolution_data, competitive_data,
             value_chain_data, distribution_data, challenges_data, kpi_data,
             regulation_data, trends_data] = results

            # Create slides list in the same order as before
            slides = [
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
            ]
            
            return slides
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating presentation: {str(e)}")

# Serve HTML form at the root
@app.get("/", response_class=HTMLResponse)
async def serve_form():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Industry Analysis Generator</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body { 
                font-family: 'Roboto', sans-serif; 
                text-align: center; 
                margin: 50px; 
                background-color: #ffffff; 
                color: #000000; 
            }
            h1 { 
                color: #000000; 
                margin-bottom: 20px; 
            }
            input, button { 
                padding: 10px; 
                font-size: 16px; 
                border: 1px solid #000000; 
                border-radius: 5px; 
                margin: 10px; 
                width: 300px; 
            }
            button { 
                background-color: #000000; 
                color: white; 
                cursor: pointer; 
                transition: background-color 0.3s; 
            }
            button:hover { 
                background-color: #444444; 
            }
            #loading { 
                display: none; 
                font-size: 18px; 
                color: #000000; 
                margin-top: 10px; 
            }
            .container {
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
        </style>
        <script>
            function showLoading(event) {
                event.preventDefault();
                document.getElementById("loading").style.display = "block";
                document.getElementById("form").submit();
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Generate Industry Analysis Presentation</h1>
            <form id="form" action="/generate-presentation" method="post">
                <input type="text" name="industry" placeholder="Enter Industry" required>
                <button type="submit" onclick="showLoading(event)">Generate</button>
            </form>
            <p id="loading">Generating... Please wait.</p>
        </div>
    </body>
    </html>
    """

# Update the endpoint to use async/await
@app.post("/generate-presentation")
async def generate_presentation(industry: str = Form(...)):
    """
    Generate a complete industry analysis presentation with glossary.
    Returns the PowerPoint file for download.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Generate presentation slides using parallel processing
        slides = await PresentationService.generate_presentation(industry)
        
        # Create markdown with glossary
        markdown_content = await PresentationService.create_markdown(slides, industry)
        
        # Save markdown file
        markdown_path = f"output/{industry}_presentation.md"
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        # Generate PowerPoint using Marp
        pptx_path = f"output/{industry}_presentation.pptx"
        command = f"marp --pptx {markdown_path} -o {pptx_path}"
        subprocess.run(command, shell=True)
        
        # Return PowerPoint file
        if os.path.exists(pptx_path):
            return FileResponse(
                pptx_path,
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                filename=f"{industry}_presentation.pptx"
            )
        else:
            raise HTTPException(status_code=500, detail="Error generating PowerPoint file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
