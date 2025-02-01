from openai import OpenAI
import json

client = OpenAI()

class TrendsService:
    @staticmethod
    def get_paragraph(prompt: str = "EV"):
        system_prompt = f"""
        You are a Powerpoint Presentation Generator
        You are assigned with a part of ppt generation
        You will be writing the content for 3 slides of ppt
        All our output text will be in markdown

        Ensure that the markdown is correctly formatted with all gaps and layout, including line breaks. 
        All tables and charts must be displayed correctly, and all headings and their subheadings should be accurate.
        
        Slide One:
        1. This slide is about recent industry trends
        2. Start with main title as "# Recent Industry Trends"
        3. Use this format for the content:
        `
        ### Recent Industry Trends

        **Increased Private Sector Participation**: Companies like SpaceX, Blue Origin, and Rocket Lab are leading advancements, driving competition, and collaborating with government space agencies like NASA and ESA.

        **Development of Reusable Spacecraft and Launch Vehicles**: Reusability is reducing costs significantly, exemplified by SpaceX's Falcon 9 and Starship programs. This shift makes space access more frequent and economical.

        **Focus on Cost Reduction in Space Transportation**: Innovations in manufacturing, materials, and modular design are decreasing launch costs, opening doors for smaller companies and startups to enter the space economy.
        `
        
        Slide Two:
        1. This slide is about expansion of services
        2. Use this format for the content:
        `
        **Expansion of Commercial Services:**

        - Satellite Internet: Projects like Starlink and Amazon's Project Kuiper aim to deliver high-speed internet to underserved areas globally.
        - Earth Observation: Companies like Planet Labs and Maxar are providing actionable insights for industries such as agriculture, disaster response, and urban planning.

        **Growing Interest in Space Tourism and Private Space Stations**:

        - Space tourism is becoming a reality, with milestones like Virgin Galactic's commercial flights and Blue Origin's suborbital journeys.
        - Plans for private space stations, such as Axiom Space's modules and Orbital Reef, aim to replace the ISS and serve as hubs for research, manufacturing, and tourism.
        `
        
        Slide Three:
        1. This slide is about industry categories
        2. Use this format for the content:
        `
        | Category | Description |
        | :---- | :---- |
        | **Reusable Rockets** | Companies like SpaceX and Blue Origin have developed reusable rockets, reducing launch costs and increasing space accessibility. |
        | **Small Satellites** | CubeSats and NanoSats are lowering barriers to entry, enabling diverse applications and creating opportunities for smaller players. |
        | **Space Tourism** | Private companies are focusing on civilian space experiences, driving growth in commercial space travel. |
        | **Advanced Space Manufacturing** | Innovations like 3D printing are enhancing production capabilities for space-based manufacturing. |
        | **Smart Propulsion** | Electric, green, and water-based propulsion systems are emerging as efficient and sustainable options for space travel. |
        | **Artificial Intelligence and Machine Learning** | AI/ML is revolutionizing satellite management, data analytics, and exploration, with the market projected to reach $1.8 trillion by 2030. |
        | **Advanced Communications** | Developments in laser communication systems and satellite technology are improving data transmission capabilities. |
        | **Space Traffic Management** | Solutions for managing space traffic and debris removal are becoming critical as orbital congestion increases. |
        | **Lunar Exploration** | Renewed focus on human missions to the Moon includes plans for sustainable presence and resource utilization. |
        | **Climate and Weather Monitoring** | Advanced satellite technologies are enhancing climate and weather monitoring, providing critical insights for Earth sciences. |
        `

        4. Adapt all content appropriately for the {prompt} industry while maintaining the same structure and format.
        """
        
        user_prompt = f"""
        Generate industry trends content for {prompt} industry following the provided format
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
                    "name": "trends_slides",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "trends_slide_1_recent_trends": { "type": "string" },
                            "trends_slide_2_expansion_services": { "type": "string" },
                            "trends_slide_3_industry_categories": { "type": "string" },
                        },
                    "required": ["trends_slide_1_recent_trends", "trends_slide_2_expansion_services", "trends_slide_3_industry_categories"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            }
        )
        
        data = json.loads(response.choices[0].message.content)
        
        # print(data["trends_slide_1_recent_trends"])
        # print(data["trends_slide_2_expansion_services"])
        # print(data["trends_slide_3_industry_categories"])
        
        return data