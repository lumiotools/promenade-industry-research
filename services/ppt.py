# from typing import List
# import json
# from Overview import OverviewService
# from Distribution import DistributionService
# from Regulation import RegulationService
# from Trends import TrendsService
# from IndustryEvolution import IndustryEvolutionService
# from ValueChain import ValueChainService 
# from CompetitiveLandscape import CompetitiveLandscapeService
# from Challenges import ChallengesService
# from Market import MarketService
# from IndustryKpi import IndustryKpiService

# class IndustryAnalysisService:
#     def __init__(self):
#         self.services = {
#             'overview': OverviewService,
#             'market': MarketService,
#             'industry_evolution': IndustryEvolutionService,
#             'competitive_landscape': CompetitiveLandscapeService,
#             'value_chain': ValueChainService,
#             'distribution': DistributionService,
#             'challenges': ChallengesService,
#             'industry_kpi': IndustryKpiService,
#             'regulation': RegulationService,
#             'trends': TrendsService
#         }
        
#     def get_service_result(self, service_name: str) -> str:
#         """Get clean result from a single service"""
#         try:
#             service = self.services.get(service_name)
#             if not service:
#                 return ""
                            
#             if service_name == 'industry_evolution':
#                 result = service.get_evolution_content()
#             elif service_name == 'competitive_landscape':
#                 result = service.get_slides()
#             elif service_name == 'industry_kpi':
#                 result = service.generate_tabular()
#             else:
#                 result = service.get_paragraph()
                
#             if isinstance(result, str):
#                 return result
#             elif isinstance(result, dict):
#                 return " ".join(str(value) for value in result.values())
#             else:
#                 return str(result)
                
#         except Exception:
#             return ""

#     def get_industry_analysis(self, industry_name: str) -> List[str]:
#         """Get analysis results as an array of strings"""
#         results = []
        
#         services_order = [
#             'overview',
#             'market', 
#             'industry_evolution',
#             'competitive_landscape',
#             'value_chain',
#             'distribution',
#             'challenges',
#             'industry_kpi',
#             'regulation',
#             'trends'
#         ]
        
#         for service_name in services_order:
#             result = self.get_service_result(service_name)
#             results.append(result)
            
#         return results

# def generate_marp_presentation(results: List[str], industry_name: str):
#     """Generate Marp presentation from results"""
#     marp_header = """---
# marp: true
# theme: gaia
# paginate: true
# ---

# <style>
# section {
#   font-size: 16px;
# }
# </style>
# """
    
#     titles = [
#         "Overview"
#         "Industry Market Size & Structure",
#         "Key Components of Industry",
#         "Major Segments",
#         "Market Segments",
#         "Core Technology Areas",
#         "Value Chain Analysis",
#         "Distribution Channels",
#         "Industry Challenges",
#         "Key Performance Indicators",
#         "Industry Trends"
#     ]
    
#     with open(f"{industry_name}_presentation.md", "w", encoding="utf-8") as f:
#         # Write header
#         f.write(marp_header + "\n")
        
#         # Write content for each section
#         for title, content in zip(titles, results):
#             f.write(f"# *{title}*\n\n")
#             f.write(content + "\n\n---\n\n")
            
#         # Store the array format in JSON as well
#         with open(f"{industry_name}_analysis_array.json", "w", encoding="utf-8") as json_file:
#             json.dump(results, json_file, indent=2)

# def main():
#     # Initialize service
#     analysis_service = IndustryAnalysisService()
    
#     # Get analysis for industry
#     industry_name = "automotive"
#     results = analysis_service.get_industry_analysis(industry_name)
    
#     # Generate Marp presentation
#     generate_marp_presentation(results, industry_name)
    
#     # Print the array format
#     print("\nComplete Array Format:")
#     print("=====================")
#     print(json.dumps(results, indent=2))
    
#     return results

# if __name__ == "__main__":
#     results = main()


from typing import List
import json
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

class IndustryAnalysisService:
    def __init__(self):
        self.services = {
            'overview': OverviewService,
            'market': MarketService,
            'industry_evolution': IndustryEvolutionService,
            'competitive_landscape': CompetitiveLandscapeService,
            'value_chain': ValueChainService,
            'distribution': DistributionService,
            'challenges': ChallengesService,
            'industry_kpi': IndustryKpiService,
            'regulation': RegulationService,
            'trends': TrendsService
        }
        
    def get_service_result(self, service_name: str) -> str:
        """Get clean result from a single service"""
        try:
            service = self.services.get(service_name)
            if not service:
                return ""
                            
            if service_name == 'industry_evolution':
                result = service.get_evolution_content()
            elif service_name == 'competitive_landscape':
                result = service.get_slides()
            elif service_name == 'industry_kpi':
                result = service.generate_tabular()
            else:
                result = service.get_paragraph()
                
            if isinstance(result, str):
                return result
            elif isinstance(result, dict):
                return " ".join(str(value) for value in result.values())
            else:
                return str(result)
                
        except Exception:
            return ""

    def get_industry_analysis(self, industry_name: str) -> List[str]:
        """Get analysis results as an array of strings"""
        results = []
        
        services_order = [
            'overview',
            'market', 
            'industry_evolution',
            'competitive_landscape',
            'value_chain',
            'distribution',
            'challenges',
            'industry_kpi',
            'regulation',
            'trends'
        ]
        
        for service_name in services_order:
            result = self.get_service_result(service_name)
            results.append(result)
            
        return results

def extract_title(content: str) -> str:
    """Extract the first line from the content to use as title"""
    if not content:
        return "No Content Available"
    
    # Split by newline and get first non-empty line
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    if not lines:
        return "No Content Available"
    
    # Remove any markdown characters from the title
    title = lines[0]
    title = title.lstrip('#').strip()
    return title

def generate_marp_presentation(results: List[str], industry_name: str):
    """Generate Marp presentation from results"""
    marp_header = """---
marp: true
theme: gaia
paginate: true
backgroundColor: white
---

<style>
section {
    font-size: 16px;
    padding: 20px;
}
h1 {
    font-size: 28px;
    margin-bottom: 20px;
}
</style>
"""
    
    with open(f"{industry_name}_presentation.md", "w", encoding="utf-8") as f:
        # Write header
        f.write(marp_header + "\n")
        
        # Title slide
        f.write(f"# {industry_name.title()} Industry Analysis\n\n")
        f.write("---\n\n")
        
        # Write content for each section
        for content in results:
            if content.strip():  # Only create slides for non-empty content
                title = extract_title(content)
                
                # Write the title
                f.write(f"# {title}\n\n")
                
                # Write the content (excluding the first line which is the title)
                content_lines = content.split('\n')
                if len(content_lines) > 1:
                    content_body = '\n'.join(line for line in content_lines[1:] if line.strip())
                    f.write(content_body + "\n\n")
                
                # Add page break
                f.write("---\n\n")
            
        # Store the array format in JSON as well
        with open(f"{industry_name}_analysis_array.json", "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, indent=2)

def main():
    # Initialize service
    analysis_service = IndustryAnalysisService()
    
    # Get analysis for industry
    industry_name = "ev"
    results = analysis_service.get_industry_analysis(industry_name)
    
    # Generate Marp presentation
    generate_marp_presentation(results, industry_name)
    
    # Print the array format
    print("\nComplete Array Format:")
    print("=====================")
    print(json.dumps(results, indent=2))
    
    return results

if __name__ == "__main__":
    results = main()