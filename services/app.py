from openai import OpenAI
import json
import subprocess

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

def generate_presentation(prompt: str = "EV") -> list:
    """
    Generates a presentation by calling all services in order and storing slides in an array.
    Each section's heading, title, or subtitle is added to the first slide of that section.
    Returns an array of 28 slides as strings.
    """
    slides = []

    overview_data = OverviewService.get_paragraph(prompt)
    slides.append(overview_data["overview_slide_1_overview_paragraph"])
    slides.append(overview_data["overview_slide_2_sector_wise_key_activities_table"])
    slides.append(overview_data["overview_slide_3_use_cases_table"])

    market_data = MarketService.get_paragraph(prompt)
    slides.append(market_data["market_slide_1_overview_paragraph"])
    slides.append(market_data["market_slide_2_sector_wise_key_activities_table"])
    slides.append(market_data["market_slide_3_major_segment"])
    slides.append(market_data["market_slide_4_market_segment_table"])
    slides.append(market_data["market_slide_5_application_table"])
    slides.append(market_data["market_slide_6_end_users_table"])
    slides.append(market_data["market_slide_7_core_technology"])

    evolution_data = IndustryEvolutionService.get_evolution_content(prompt)
    slides.append(evolution_data["industry_evolution_slide_1_evolution_overview"] + "\n\n" +   evolution_data["industry_evolution_slide_2_timeline"]) 
    slides.append(evolution_data["industry_evolution_slide_3_future_trends"])

    competitive_landscape_data = CompetitiveLandscapeService.get_slides(prompt)
    slides.append(competitive_landscape_data["competitive_landscape_slide_1_overview"])
    slides.append(competitive_landscape_data["competitive_landscape_slide_2_factors"])

    value_chain_data = ValueChainService.get_paragraph(prompt)
    slides.append(value_chain_data)

    distribution_data = DistributionService.get_paragraph(prompt)
    slides.append(distribution_data["distribution_slide_1_end_customers"])
    slides.append(distribution_data["distribution_slide_2_distribution_models_and_partners"])
    slides.append(distribution_data["distribution_slide_3_emerging_channels"])

    challenges_data = ChallengesService.get_paragraph(prompt)
    slides.append(challenges_data["challenges_slide_1_challenges_and_opportunities_paragraph"])

    kpi_data = IndustryKpiService.generate_tabular(prompt)
    slides.append(kpi_data["industry_kpi_slide_1_industry_kpi_table"])

    regulation_data = RegulationService.get_paragraph(prompt)
    slides.append(regulation_data["regulation_silde_1_regulatory_bodies"])
    slides.append(regulation_data["regulation_silde_2_key_regulations"])
    slides.append(regulation_data["regulation_silde_3_licensing_requirements"])

    trends_data = TrendsService.get_paragraph(prompt)
    slides.append(trends_data["trends_slide_1_recent_trends"])
    slides.append(trends_data["trends_slide_2_expansion_services"])
    slides.append(trends_data["trends_slide_3_industry_categories"])

    assert len(slides) == 26, f"Expected 28 slides, but got {len(slides)}"

    return slides


def create_marp_markdown(slides: list, industry_name: str):
    """
    Creates a Marp Markdown file from the slides array.
    Each slide is separated by a slide break (`---`).
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
</style>
"""

    with open(f"{industry_name}_presentation.md", "w", encoding="utf-8") as file:
        file.write(marp_header + "\n")

        file.write(f"# {industry_name.title()} Industry Analysis\n\n")
        file.write("---\n\n")

        for slide in slides:
            file.write(slide + "\n\n")
            file.write("---\n\n")

    print(f"Marp Markdown presentation saved to '{industry_name}.md'")


# Example usage
if __name__ == "__main__":
    prompt = "AI"
    presentation_slides = generate_presentation(prompt)

    with open(f"{prompt}_slides.json", "w") as json_file:
        json.dump(presentation_slides, json_file, indent=4)
    print(f"Slides saved to '{prompt}_slides.json'")

    with open(f"{prompt}_slides.txt", "w") as text_file:
        for i, slide in enumerate(presentation_slides, 1):
            text_file.write(f"Slide {i}:\n{slide}\n\n")
    print(f"Slides saved to '{prompt}_slides.txt'")

    create_marp_markdown(presentation_slides, prompt)

    command = f"marp --pptx {prompt}_presentation.md -o {prompt}_presentation.pptx"
    subprocess.run(command, shell=True)
    print(f"Executed command: {command}")