from openai import OpenAI
import json
import subprocess
import re

client = OpenAI()

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
    def extract_terms_from_markdown(markdown_file_path: str) -> list:
        """
        Extracts technical terms and phrases from a markdown file.
        Returns a list of terms.
        """
        try:
            with open(markdown_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
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
        
        except Exception as e:
            print(f"Error extracting terms from markdown: {str(e)}")
            return []

    @staticmethod
    def split_glossary_content(content: str) -> list:
        """
        Splits glossary content into multiple slides.
        Each letter group will be on its own slide.
        """
        slides = []
        
        # Handle empty or error content
        if not content or content == "# Glossary\n\nNo technical terms found in the presentation.":
            return [content]

        # Split by letter sections
        letter_sections = content.split('\n\n**')[1:]  # Skip the header
        current_slide = []
        current_length = 0
        
        for section in letter_sections:
            section_content = f"**{section}"
            lines = len(section_content.split('\n'))
            
            if current_length + lines > 10 or not current_slide:  # Max 10 lines per slide
                if current_slide:
                    slides.append("# Glossary\n\n" + "\n\n".join(current_slide))
                current_slide = [section_content]
                current_length = lines
            else:
                current_slide.append(section_content)
                current_length += lines
        
        if current_slide:
            slides.append("# Glossary\n\n" + "\n\n".join(current_slide))
        
        return slides if slides else ["# Glossary\n\nNo terms to display"]

    @staticmethod
    def get_glossary(markdown_file_path: str) -> dict:
        """
        Generates a glossary from terms found in the markdown file.
        Returns dictionary with multiple glossary slides.
        """
        terms = GlossaryService.extract_terms_from_markdown(markdown_file_path)
        
        if not terms:
            return {"glossary_slides": ["# Glossary\n\nNo technical terms found in the presentation."]}
        
        system_prompt = """
        You are a technical glossary generator. Create definitions for the provided technical terms.
        Format the output as a markdown glossary organized alphabetically.
        """
        
        user_prompt = f"""
        Create a glossary for these technical terms: {', '.join(terms)}
        
        Limit the glossary to a maximum of 5 important words for each letter.
        
        Format as:
        # Glossary

        **A**
        * **Term1**: Definition
        * **Term2**: Definition

        Only include letters that have associated terms.
        Organize terms alphabetically under their respective letters.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            content = response.choices[0].message.content
            glossary_slides = GlossaryService.split_glossary_content(content)
            
            return {"glossary_slides": glossary_slides}
            
        except Exception as e:
            print(f"Error generating glossary: {str(e)}")
            return {"glossary_slides": ["# Glossary\n\nError generating content"]}

def generate_presentation(prompt: str = "EV") -> list:
    """
    Generates a presentation by calling all services in order and storing slides in an array.
    """
    slides = []

    # Overview section
    overview_data = OverviewService.get_paragraph(prompt)
    slides.append(overview_data["overview_slide_1_overview_paragraph"])
    slides.append(overview_data["overview_slide_2_sector_wise_key_activities_table"])
    slides.append(overview_data["overview_slide_3_use_cases_table"])

    # Market section
    market_data = MarketService.get_paragraph(prompt)
    slides.append(market_data["market_slide_1_overview_paragraph"])
    slides.append(market_data["market_slide_2_sector_wise_key_activities_table"])
    slides.append(market_data["market_slide_3_major_segment"])
    slides.append(market_data["market_slide_4_market_segment_table"])
    slides.append(market_data["market_slide_5_application_table"])
    slides.append(market_data["market_slide_6_end_users_table"])
    slides.append(market_data["market_slide_7_core_technology"])

    # Industry Evolution section
    evolution_data = IndustryEvolutionService.get_evolution_content(prompt)
    slides.append(evolution_data["industry_evolution_slide_1_evolution_overview"] + "\n\n" + evolution_data["industry_evolution_slide_2_timeline"]) 
    slides.append(evolution_data["industry_evolution_slide_3_future_trends"])

    # Competitive Landscape section
    competitive_landscape_data = CompetitiveLandscapeService.get_slides(prompt)
    slides.append(competitive_landscape_data["competitive_landscape_slide_1_overview"])
    slides.append(competitive_landscape_data["competitive_landscape_slide_2_factors"])

    # Value Chain section
    value_chain_data = ValueChainService.get_paragraph(prompt)
    slides.append(value_chain_data)

    # Distribution section
    distribution_data = DistributionService.get_paragraph(prompt)
    slides.append(distribution_data["distribution_slide_1_end_customers"])
    slides.append(distribution_data["distribution_slide_2_distribution_models_and_partners"])
    slides.append(distribution_data["distribution_slide_3_emerging_channels"])

    # Challenges section
    challenges_data = ChallengesService.get_paragraph(prompt)
    slides.append(challenges_data["challenges_slide_1_challenges_and_opportunities_paragraph"])

    # Industry KPI section
    kpi_data = IndustryKpiService.generate_tabular(prompt)
    slides.append(kpi_data["industry_kpi_slide_1_industry_kpi_table"])

    # Regulation section
    regulation_data = RegulationService.get_paragraph(prompt)
    slides.append(regulation_data["regulation_silde_1_regulatory_bodies"])
    slides.append(regulation_data["regulation_silde_2_key_regulations"])
    slides.append(regulation_data["regulation_silde_3_licensing_requirements"])

    # Trends section
    trends_data = TrendsService.get_paragraph(prompt)
    slides.append(trends_data["trends_slide_1_recent_trends"])
    slides.append(trends_data["trends_slide_2_expansion_services"])
    slides.append(trends_data["trends_slide_3_industry_categories"])

    return slides

def create_marp_markdown(slides: list, industry_name: str) -> str:
    """
    Creates a Marp Markdown file from the slides array.
    Each slide is separated by a slide break (`---`).
    Returns the path to the created markdown file.
    """
    marp_header = """---
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

    markdown_file_path = f"{industry_name}_presentation.md"
    
    with open(markdown_file_path, "w", encoding="utf-8") as file:
        file.write(marp_header + "\n")
        
        # Title slide
        file.write(f"# {industry_name.title()} Industry Analysis\n\n")
        file.write("---\n\n")
        
        # Content slides
        for slide in slides:
            file.write(slide + "\n\n")
            file.write("---\n\n")
    
    print(f"Marp Markdown presentation saved to '{markdown_file_path}'")
    return markdown_file_path

def save_outputs(slides: list, prompt: str) -> None:
    """
    Saves the slides to JSON and TXT formats
    """
    # Save to JSON
    with open(f"{prompt}_slides.json", "w", encoding="utf-8") as json_file:
        json.dump(slides, json_file, indent=4)
    print(f"Slides saved to '{prompt}_slides.json'")

    # Save to TXT
    with open(f"{prompt}_slides.txt", "w", encoding="utf-8") as text_file:
        for i, slide in enumerate(slides, 1):
            text_file.write(f"Slide {i}:\n{slide}\n\n")
    print(f"Slides saved to '{prompt}_slides.txt'")

def main(prompt: str = "AI"):
    """
    Main execution function that coordinates the presentation generation process
    """
    try:
        # Generate initial slides
        print(f"Generating presentation for {prompt} industry...")
        presentation_slides = generate_presentation(prompt)
        
        # Create initial markdown file
        print("Creating initial markdown file...")
        markdown_file_path = create_marp_markdown(presentation_slides, prompt)
        
        # Generate glossary from markdown
        print("Generating glossary...")
        glossary_data = GlossaryService.get_glossary(markdown_file_path)
        
        # Add all glossary slides
        print("Adding glossary slides...")
        presentation_slides.extend(glossary_data["glossary_slides"])
        
        # Create final markdown with glossary
        print("Creating final markdown with glossary...")
        final_markdown_path = create_marp_markdown(presentation_slides, prompt)
        
        # Save outputs
        print("Saving outputs...")
        save_outputs(presentation_slides, prompt)
        
        # Generate PowerPoint
        print("Generating PowerPoint presentation...")
        command = f"marp --pptx {final_markdown_path} -o {prompt}_presentation.pptx"
        subprocess.run(command, shell=True)
        print(f"PowerPoint presentation generated: {prompt}_presentation.pptx")
        
        return "Presentation generation completed successfully!"
        
    except Exception as e:
        print(f"Error during presentation generation: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    prompt = "AI"
    result = main(prompt)
    print(result)