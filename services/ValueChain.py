from openai import OpenAI
import json

client = OpenAI()

class ValueChainService:
    @staticmethod
    def get_paragraph(prompt: str = "EV"):
        system_prompt = f"""
        You are a Powerpoint Presentation Generator
        You will be writing the content for a single slide
        All output text will be in markdown

        Ensure that the markdown is correctly formatted with all gaps and layout, including line breaks. 
        All tables and charts must be displayed correctly, and all headings and their subheadings should be accurate.
        
        The slide should:
        1. Start with the title "### {prompt} Industry Value Chain and Operations**"
        2. Follow with a brief introductory paragraph explaining the five key segments
        3. Then provide detailed descriptions of each segment on new lines with two spaces for line breaks
        4. End with a concluding statement about how these segments work together
        5. Use this exact format:
        
        **{prompt} Industry Value Chain and Operations**

        The {prompt} industry value chain encompasses five key segments: Research and Development (R&D), Manufacturing and Assembly, Launch Services, Satellite Operations, and End-User Support and Services.

        R&D focuses on innovation, concept development, and prototype testing, often in collaboration with academia and governed by regulatory compliance.  
        Manufacturing and assembly involve the production of spacecraft and satellite components, system integration, quality control, and supply chain management.  
        Launch services include preparing and executing launches, payload integration, and post-launch analysis.  
        Satellite operations ensure the efficient design, management, and maintenance of satellites, including data transmission and end-of-life disposal.  
        Lastly, end-user support provides customer assistance, training, documentation, and service level agreements, fostering continuous feedback and improvement. Together, these segments create a cohesive framework that drives the development, deployment, and utilization of space technologies.
        """
        
        user_prompt = f"""
        Generate value chain content for {prompt} industry following the exact format provided
        """
        
        try:
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
                        "name": "value_chain_slide",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "slide_content": { "type": "string" }
                            },
                            "required": ["slide_content"],
                            "additionalProperties": False,
                        },
                        "strict": True,
                    },
                }
            )
            
            data = json.loads(response.choices[0].message.content)
            print(data["slide_content"])
            return data["slide_content"]
            
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None
