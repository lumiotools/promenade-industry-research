from  openai import OpenAI
import json

client=OpenAI()

class OverviewService:
        
    def get_paragraph(prompt: str="EV"):
        
        system_prompt = f"""
        You are a Powerpoint Presentation Generator
        You are assigned with a part of ppt generation
        You will be writing the content for 3 slides of ppt
        All our output text will be in markdown
        
        Slide One:
        1. This slide is an overview page
        2. In this page we need to write some paragraphs based on user query
        3. This is the sample Overview Paragraphs for User Query `SpaceTech Industry`:
            `
            ** Overview of the {prompt} Industry **

            The SpaceTech industry is undergoing significant growth and transformation. In 2023, the global space technology market was valued at USD 433.25 billion and is projected to reach USD 700.28 billion by 2030, with a CAGR of 7.1%. This expansion is fueled by technological innovation, increased private sector participation, and enhanced government initiatives.

            **Rapid Market Growth**: The global space technology market is forecasted to grow from USD 433.25 billion in 2023 to USD 501.46 billion by 2025, achieving a CAGR of 8.4% from 2024\.

            **Private Sector Involvement**: Increasing participation from private companies is accelerating market expansion, driven by innovations in reusable rockets, satellite services, and space tourism.

            **Government Initiatives**: National programs continue to invest heavily in space exploration and infrastructure, fostering public-private collaborations.

            **Emerging Technologies**: The integration of AI in space exploration is creating new opportunities. The AI in space market is projected to grow from USD 3.4 billion in 2023 to USD 4.44 billion by 2024, reflecting rapid adoption of AI for mission planning, data analysis, and autonomous operations.

            SpaceTech is a comprehensive industry focused on developing and applying technologies for space exploration, research, and commercial activities. It encompasses a wide range of technological solutions and economic activities related to outer space exploration and utilization.

            The SpaceTech industry is divided into two primary sectors: upstream and downstream. The upstream sector focuses on activities related to getting objects into space, such as the development and manufacturing of spacecraft, satellites, and launch vehicles, as well as space exploration and ground station operations. In contrast, the downstream sector deals with the utilization of space technologies, including satellite-based applications, Earth observation services, communication systems, and data-driven services derived from these technologies. Together, these sectors form a comprehensive ecosystem driving innovation and value creation in SpaceTech.
            `
        4. The above sample explain the exact format of the required overview paragraph.
        5. Limit the content to max 300 words.
        6. Start with main title as "###Overview", and then use heading "**Overview of the {prompt} Industry**"
        
        Slide Two:
        1. This slide is sector wise key activities page in tabular form
        2. In this slide we need some tabular data based on user query
        3. This is the sample Sector wise key activities for User Query `SpaceTech Industry`:
        `
        | Sector | Key Activities |
        | :---- | :---- |
        | **Upstream Sector** | \- Transportation of objects into space \- Ground stations \- Space exploration \- Manufacturing of spacecraft, satellites, and launch vehicles |
        | **Downstream Sector** | \- Data and services derived from space technologies \- Satellite-based applications \- Earth observation services \- Communication systems |
        `
        4. The above sample explain the exact format of the required sector wise key activities table.
        
        Slide Three:
        1. This slide is use cases page
        2. In this slide we need some use cases based on user query
        3. This is the sample Use Cases for User Query `SpaceTech Industry`:
        `
        SpaceTech is used across the following use cases:

        | Application Area | Description |
        | :---- | :---- |
        | **Navigation and Mapping** | Provides GPS and satellite-based navigation for transportation, logistics, and geographic mapping. |
        | **Meteorology** | Enables weather forecasting and climate monitoring using satellite data. |
        | **Disaster Management** | Supports monitoring and management of natural disasters, such as floods, hurricanes, and earthquakes. |
        | **Satellite Communication** | Facilitates global communication networks, including telephone and data transfer services. |
        | **Satellite Television** | Provides television broadcasting and content delivery to global audiences via satellites. |
        | **Remote Sensing** | Collects data for applications such as agriculture, urban planning, and environmental monitoring. |
        | **Scientific Research and Engineering** | Advances understanding in fields like astronomy, space exploration, and material science. |
        | **Military and National Security** | Enhances surveillance, reconnaissance, and secure communication for defense purposes. |
        | **Internet Services** | Offers high-speed internet access globally, including underserved and remote regions. |
        `
        4. The above sample explain the exact format of the required use cases table.
        """
        
        user_prompt = f"""
        Give me the overview of {prompt}
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
                        "slide_1_overview_paragraph": { "type": "string" },
                        "slide_2_sector_wise_key_activities_table": { "type": "string" },
                        "slide_3_use_cases_table": { "type": "string" },
                    },
                    "required": ["slide_1_overview_paragraph", "slide_2_sector_wise_key_activities_table", "slide_3_use_cases_table"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
        )
        
        data = json.loads(response.choices[0].message.content)
        
        print(data["slide_1_overview_paragraph"])
        print(data["slide_2_sector_wise_key_activities_table"])
        print(data["slide_3_use_cases_table"])

        return data
        