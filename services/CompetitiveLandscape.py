from openai import OpenAI
import json

client = OpenAI()

class CompetitiveLandscapeService:
    @staticmethod
    def get_slides(prompt: str = "EV"):
        system_prompt = f"""
        You are a Powerpoint Presentation Generator
        You will be writing content for 2 slides
        All output text will be in markdown

        Ensure that the markdown is correctly formatted with all gaps and layout, including line breaks. 
        All tables and charts must be displayed correctly, and all headings and their subheadings should be accurate.

        A competitive landscape analysis is crucial for understanding market dynamics, identifying key players, and evaluating competitive advantages in the {prompt} industry. This analysis examines established companies, emerging players, market share distribution, and critical competitive factors shaping the industry.
        
        Slide One Format:
        `
        ### Competitive Landscape

        **Established Aerospace Companies**: Traditional players like Boeing, Lockheed Martin, and Airbus SE continue to hold significant market share.

        **Emerging Private Companies**: SpaceX, Blue Origin, and Virgin Galactic have disrupted the market with innovative approaches and reusable rocket technology.

        **Government Space Agencies**: NASA, ISRO, and China Aerospace Science and Technology Corporation remain influential in space exploration and research.

        **Satellite Communications**: Companies like SES S.A., Viasat Inc., and Eutelsat Communications SA compete in the growing satellite services market.

        **Profiles of Key Players**

        The {prompt} market is moderately concentrated, with several key players dominating various segments:

        Space vehicles segment dominated the market in 2022 with a share of more than 66%1.

        Major players include NASA, SpaceX, Blue Origin, Northrop Grumman, Lockheed Martin, Boeing, and Airbus SE34.
        `

        Slide Two Format:
        `
        **Competitive Factors**

        | Factor | Description |
        | :---- | :---- |
        | **Technological Innovation** | Development of cutting-edge technologies such as reusable rockets, advanced spacecraft, satellite systems, and AI-based space applications is driving intense competition. Companies that innovate faster and more efficiently gain a competitive edge by reducing operational costs, increasing reliability, and enabling new applications. Examples include SpaceX's Falcon 9 and Starship, which have revolutionized cost and reusability. |
        | **Cost Reduction** | Lowering launch and operational costs is critical to gaining market share. SpaceX has set industry benchmarks by reducing launch costs to as low as $2,600 per kilogram through reusability. This has forced competitors like Blue Origin and Rocket Lab to focus on similar strategies to remain competitive. The drive for cost reduction also enables smaller companies to enter the market, increasing overall competition. |
        | **Commercialization** | Private sector involvement has expanded rapidly, with companies diversifying revenue streams through satellite services (e.g., Starlink), space tourism (Virgin Galactic, Blue Origin), and in-space manufacturing. The focus on commercial services has opened new opportunities but also increased competition as companies vie for contracts and partnerships with governments, corporations, and other private entities. |
        | **Geographic Expansion** | The Asia Pacific region is emerging as a significant player in spacetech, driven by government investments (e.g., India's ISRO, China's CNSA) and private-sector growth. With a projected CAGR of over 9% from 2023 to 2030, this region is poised to challenge the dominance of the U.S. and Europe. Companies expanding their presence in these markets must navigate regional regulations, talent pools, and infrastructure challenges. |
        `

        Note: Generate the content maintaining industry-specific context, accurate company names, and relevant competitive factors for the {prompt} sector.
        """
        
        user_prompt = f"""
        Based on the competitive landscape analysis introduction, generate two detailed slides for the {prompt} industry following the exact format provided. Ensure the content reflects current market dynamics and competitive factors specific to this sector.
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
                    "name": "competitive_landscape_slides",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "slide_1_overview": { "type": "string" },
                            "slide_2_factors": { "type": "string" }
                        },
                        "required": ["slide_1_overview", "slide_2_factors"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            }
        )
        
        data = json.loads(response.choices[0].message.content)
        
        print(data["slide_1_overview"])
        print(data["slide_2_factors"])
        
        return data
