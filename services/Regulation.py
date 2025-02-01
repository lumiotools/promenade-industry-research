from openai import OpenAI
import json

client = OpenAI()

class RegulationService:
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
        1. This slide is about regulations and regulatory bodies
        2. Start with main title as "# Regulation"
        3. Use this format for the regulatory bodies content:
        `
        ### SpaceTech Industry Regulatory Bodies

        | Organization | Responsibility |
        | :---- | :---- |
        | Federal Aviation Administration (FAA) | Regulates commercial spaceflight and launch services. |
        | Federal Communications Commission (FCC) | Oversees radio frequency allocations for satellites and orbital debris mitigation. |
        | National Oceanographic and Atmospheric Administration (NOAA) | Regulates remote sensing activities, including Earth observation systems. |
        | Department of Commerce | Potentially responsible for Space Traffic Management, ensuring safe and sustainable use of orbital resources. |
        `
        
        Slide Two:
        1. This slide is about key regulations
        2. Use this format for the key regulations content:
        `
        ### Key Regulations for the SpaceTech Industry

        | Policy/Regulation | Description |
        | :---- | :---- |
        | Commercial Space Launch Act (USA) | Mandates licensing for commercial space launches and re-entries, regulated by the FAA's Office of Commercial Space Transportation. |
        | FCC Regulations (USA) | Governs the allocation of radio spectrum and licensing for Earth and space stations used in satellite communications. |
        | NOAA Regulations (USA) | Requires special permits for satellites with remote sensing capabilities. |
        | Commercial Space Act of 2023 (USA) | Adopts a laissez-faire approach to debris mitigation, requiring commercial operators to submit mitigation plans. |
        | Satellite Communication Policy (1997) | Provides guidelines for satellite communication services in India, including licensing procedures and spectrum allocation. |
        | Revised Remote Sensing Data Policy (2011) | Regulates the collection, dissemination, and use of satellite remote sensing data in India. |
        | Geospatial Guidelines (2021) | Liberalizes geospatial data access and utilization, promoting ease of use of satellite-generated data in India. |
        | International Treaties | Includes the Outer Space Treaty (1967), Agreement on the Rescue of Astronauts (1968), and Liability Convention (1972), to which India is a signatory. |
        `
        
        Slide Three:
        1. This slide is about licensing requirements
        2. Use this format for the licensing requirements content:
        `
        ### Licensing Requirements and Compliance in the SpaceTechIndustry

        **Federal Aviation Administration (FAA)**:
        Vehicle Operator License: Required for launches or re-entries using the same vehicle or family of vehicles.
        
        **Spaceport License**: Needed for operating a launch or reentry site.
        
        **Experimental Permit**: Authorizes unlimited launches or re-entries of a reusable suborbital rocket for one year.
        
        **National Oceanic and Atmospheric Administration (NOAA)**:
        Commercial Remote Sensing License: Required for satellites with remote sensing capabilities.
        
        **Federal Communications Commission (FCC)**:
        Space Station License: Needed for satellite communications and spectrum use.
        
        **Earth Station License**: Required for ground-based communication with satellites
        `

        4. Adapt all content appropriately for the required industry while maintaining the same structure and format.
        """
        
        user_prompt = f"""
        Generate regulatory content for {prompt} industry following the provided format
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
                    "name": "regulation_sildes",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "regulation_silde_1_regulatory_bodies": { "type": "string" },
                            "regulation_silde_2_key_regulations": { "type": "string" },
                            "regulation_silde_3_licensing_requirements": { "type": "string" },
                        },
                    "required": ["regulation_silde_1_regulatory_bodies", "regulation_silde_2_key_regulations", "regulation_silde_3_licensing_requirements"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            }
        )
        
        data = json.loads(response.choices[0].message.content)
        
        # print(data["regulation_silde_1_regulatory_bodies"])
        # print(data["regulation_silde_2_key_regulations"])
        # print(data["regulation_silde_3_licensing_requirements"])
        
        return data