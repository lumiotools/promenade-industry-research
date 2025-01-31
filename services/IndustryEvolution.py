from openai import OpenAI
import json

client = OpenAI()

class IndustryEvolutionService:
    @staticmethod
    def get_evolution_content(prompt: str = "EV"):
        system_prompt = f"""
        You are a Powerpoint Presentation Generator
        You are assigned with a part of ppt generation
        You will be writing the content for 3 slides of ppt
        All our output text will be in markdown

        Ensure that the markdown is correctly formatted with all gaps and layout, including line breaks. 
        All tables and charts must be displayed correctly, and all headings and their subheadings should be accurate.
        
        Slide One:
        1. This slide is about industry evolution overview
        2. Start with main title as "### {prompt} Industry Evolution and Key Milestones"
        3. Write a comprehensive paragraph about the industry's evolution through different eras
        4. Use this format for the regulatory bodies content:
        `
        The evolution of space exploration has progressed through distinct phases. In the early foundations (1950s-1960s), milestones like the launch of Sputnik 1 (1957), the establishment of NASA (1958), and the Apollo 11 Moon landing (1969) set the stage for space innovation. Commercialization began in the 1980s-1990s with key achievements such as the first privately owned rocket, Conestoga I (1982), the rise of Arianespace, and legislative support like the U.S. Commercial Space Launch Act. The 2000s-2010s saw rapid private sector growth with SpaceX's founding (2002) and pioneering feats, including the first private spacecraft recovery (2010) and berthing with the ISS (2012). Recent developments highlight SpaceX's dominance, sending humans to space in 2020, alongside trends in reusable spacecraft, cost reduction, commercial services, and space tourism, marking a transformative era in space exploration. 
        `
        
        Slide Two:
        1. This slide contains a detailed timeline table
        2. Use this format for the timeline content:
        `
        | Era | Year | Key Events |
        | :---- | :---- | :---- |
        | Early Foundations | Year | Description of milestone |
        | Growth Phase | Year | Description of milestone |
        | Modern Era | Year | Description of milestone |
        `
        
        Slide Three:
        1. This slide focuses on future trends
        2. Use this format for the future trends content:
        `
        **Future Trends in the {prompt} Industry**

        | Trend Category | Description | Expected Impact |
        | :---- | :---- | :---- |
        | Technology | Description of technological trend | Projected impact |
        | Market | Description of market trend | Projected impact |
        | Regulation | Description of regulatory trend | Projected impact |
        | Innovation | Description of innovation trend | Projected impact |
        `

        4. Adapt all content appropriately for the {prompt} industry while maintaining the same structure and format.
        """
        
        user_prompt = f"""
        Generate industry evolution content for {prompt} industry following the provided format
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",                   
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "evolution_slides",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "industry_evolution_slide_1_evolution_overview": { "type": "string" },
                            "industry_evolution_slide_2_timeline": { "type": "string" },
                            "industry_evolution_slide_3_future_trends": { "type": "string" },
                        },
                    "required": ["industry_evolution_slide_1_evolution_overview", "industry_evolution_slide_2_timeline", "industry_evolution_slide_3_future_trends"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            }
        )
        
        data = json.loads(response.choices[0].message.content)
        
        print(data["industry_evolution_slide_1_evolution_overview"])
        print(data["industry_evolution_slide_2_timeline"])
        print(data["industry_evolution_slide_3_future_trends"])
        
        return data