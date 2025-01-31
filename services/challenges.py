from openai import OpenAI
import json

client = OpenAI()

class ChallengesService:
    
    def get_paragraph(prompt: str="EV"):
        system_prompt=f"""
        You are a PowerPoint Presentation Generator
        You are assigned with a part of ppt generation
        You will be writing the content for 1 slides of ppt
        All our output text will be in markdown

        Ensure that the markdown is correctly formatted with all gaps and layout, including line breaks. 
        All tables and charts must be displayed correctly, and all headings and their subheadings should be accurate.
        
        Slide One:
        1. This slide is challenges and opportunities page
        2. In this page we need to write some paragraph based on user query
        3. This is the sample challenges and opportunities for User Query
        `SpaceTech Industry`:
        
        `
        **Challenges and Opportunities**

        The SpaceTech industry faces significant challenges in data distribution, particularly in handling the unprecedented volume of information generated by modern satellite systems. For instance, the Copernicus Sentinel-1 satellite alone produces around 3 terabytes of data per day. This data deluge creates opportunities for innovation in distribution models, particularly in areas such as:

        - Data flow management  
        - Secure storage solutions  
        - Efficient data processing techniques  
        - Novel data brokering services

        As the SpaceTech industry continues to grow, with projections estimating a market value of $442 billion by 20252, distribution models will need to evolve to handle increasing data volumes while ensuring efficiency, security, and accessibility for a diverse range of users.
        `
        
        4. The above sample explain the exact format of the required challenges and opportunities paragraph.
        5. Limit the content to max 200 words
        6. Start with main title as "### Challenges and Opportunities" for complete slides. 
        """
        
        user_prompt=f"""
        Give me the challenges and opportunities for {prompt}
        """
        
        response = client.chat.completions.create(
             model="gpt-4o-mini",
            messages=[
                {
                    "role":"system",
                    "content":system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "overview_slides",
                "schema": {
                    "type": "object",
                    "properties": {
                        "challenges_slide_1_challenges_and_opportunities_paragraph": { "type": "string" },
                    },
                    "required": ["challenges_slide_1_challenges_and_opportunities_paragraph"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
        )
        
        data = json.loads(response.choices[0].message.content)
        
        print(data["challenges_slide_1_challenges_and_opportunities_paragraph"])

        return data