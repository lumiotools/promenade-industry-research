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
                
            # Clean the result
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

def main():
    # Initialize service
    analysis_service = IndustryAnalysisService()
    
    # Get analysis for automotive industry
    industry_name = "automotive"
    results = analysis_service.get_industry_analysis(industry_name)
    
    # Store individual results in txt file
    with open(f"{industry_name}_analysis.txt", "w", encoding="utf-8") as f:
        for result in results:
            f.write(result + "\n\n")
    
    # Store array format in json file
    with open(f"{industry_name}_analysis_array.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    # Print individual elements
    print("Individual Elements:")
    print("===================")
    for i, result in enumerate(results):
        print(f"\nArray Element {i}:")
        print(result)
        print("-" * 50)
    
    # Print array format
    print("\nComplete Array Format:")
    print("=====================")
    print(json.dumps(results, indent=2))
    
    return results

if __name__ == "__main__":
    results = main()