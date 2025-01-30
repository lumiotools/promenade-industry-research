# from perplexityai import Perplexity
from openai import OpenAI
import json

# client1 = Perplexity()
client2 = OpenAI()

class MarketService:
    
    def get_paragraph(prompt: str="EVIndustry"):
        
        system_prompt1 = f"""
        You are a PowerPoint Presentation Generator
        You are assigned with a part of ppt generation
        You will be writing the content for 8 slides of ppt 
        All our output text will be in markdown
        
        Slide One:
        1. This slide is an Industry Market Size & Structure page
        2. In this page we need to write some paragraphs based on user query
        3. This is the sample Overview Paragraphs for User Query 
        `SpaceTech Industry`:
        `
            **Employment**: Over 3.5 million workers, with 184,000 new employees added in the past year

            **Companies**: More than 35,000 companies listed in the industry

            **Patents and Grants**: Over 60,000 patents and more than 10,000 grants

            **Investment**: Average investment value of USD 61.5 million per funding round

            **Key Components of SpaceTech**

            The SpaceTech industry is divided into two primary sectors: upstream and downstream. The upstream sector focuses on activities related to getting objects into space, such as the development and manufacturing of spacecraft, satellites, and launch vehicles, as well as space exploration and ground station operations. In contrast, the downstream sector deals with the utilization of space technologies, including satellite-based applications, Earth observation services, communication systems, and data-driven services derived from these technologies. Together, these sectors form a comprehensive ecosystem driving innovation and value creation in SpaceTech.
        `
        
        4.  4. The above sample explain the exact format of the required Industry Market Size & Structure paragraph.
        5. Limit the content to max 300 words
        
        Slide Two:
        1. This slide is sector wise key activities page in tabular form
        2. In this slide we need some tabular data based on user query
        3. This is the sample Sector wise key activities for Query User 
        `SpaceTech Industry`:
        `
            | Sector | Key Activities |
            | :---- | :---- |
            | **Upstream Sector** | \- Transportation of objects into space \- Ground stations \- Space exploration \- Manufacturing of spacecraft, satellites, and launch vehicles |
            | **Downstream Sector** | \- Data and services derived from space technologies \- Satellite-based applications \- Earth observation services \- Communication systems |
        `
        
        4. The above sample explain the exact format of the required sector wise key activities table.
        
        Slide Three:
        1. This slide is major segments within the spacetech industry page
        2. In this slide we need some major segments within the spacetech industry based on user query
        3. This is the sample Major Segments within the Spacetech Industry for User Query `SpaceTech Industry`:
        `
            **Major Segments within the SpaceTech Industry**

            **Space Services**: This segment focuses on providing various services supporting space-related technologies and infrastructure. It includes:

            - Launch services for satellites and spacecraft  
            - Space-based communications (satellite internet, TV, radio)  
            - Satellite imagery and remote sensing  
            - Space-based navigation and positioning (e.g., GPS)  
            - Space weather monitoring and forecasting  
            - Space debris monitoring and mitigation

            **Space Technologies**: This segment involves the development and application of advanced technologies for space exploration, research, and commercial activities1. Key areas include:

            - Research and development of propulsion systems, materials science, and robotics  
            -  Development of satellite and space-based systems  
            -  Manufacturing of launch vehicles and rockets  
            -  Development of space habitats and infrastructure

            **Space Development**: This segment focuses on the broader aspects of space exploration and utilization.

            - **Space Manufacturing**: This appears to be one of the largest sectors within the industry.  
            -  **Satellite Communication**: Another major sector, alongside Space Manufacturing.  
            - **Space Observation**: A significant subsector within the industry.  
            - **Space Travel & Exploration**: This segment includes activities related to human spaceflight and exploration missions.  
            - **Security & Defense**: This segment involves space-based technologies for national security and defense purposes.
        `
        
        4. The above sample explain the exact format of the required major segments within the spacetech industry paragraph.
        
        Slide Four:
        1. This slide is market segments page in tabular form.
        2. In this slide we need some tabular data based on user query
        3. This is the sample Market Segments for User Query `SpaceTech Industry`:
        `
            **Market Segments**

            | Category | Description |
            | :---- | :---- |
            | **Space Vehicles** | Dominated the market in 2022 with a 66% share, highlighting their central role in the industry. |
            | **Satellites** | Essential for communication, navigation, Earth observation, and various commercial and defense applications. |
            | **Launch Vehicles** | Includes advanced technologies such as reusable rocket systems, reducing costs and increasing accessibility to space. |
            | **Spacecraft** | Vehicles designed for specific missions, including exploration, research, and habitation. |
            | **Ground Systems and Infrastructure** | Supports mission operations, including tracking, data processing, and communication networks. |
            | **Space Exploration Technologies** | Cutting-edge tools and systems enabling deep-space exploration and new scientific discoveries. |
        `
        
        4. The above sample explain the exact format of the required market segments table.
        
        Slide Five:
        1. This slide is Core Technology Area page.
        2. In this page we need to write some paragraphs based on user query
        3. This is the sample Core Technology Area for User Query `SpaceTech Industry`:
        `
            **Core Technology Areas**

            The SpaceTech industry plays a critical role in enabling essential everyday services, such as weather forecasting, satellite navigation systems, remote sensing, and long-distance communications. Beyond these applications, it drives advancements in scientific research, supporting discoveries in astronomy and Earth sciences. Far from being limited to traditional space exploration, the industry integrates cutting-edge technologies from various fields, including robotics, artificial intelligence, materials science, and advanced manufacturing. This multidisciplinary approach not only expands the possibilities of space exploration but also enhances its impact on life here on Earth.
        `
        
        4. The above sample explain the exact format of the required core technology area paragraph.
        5. Limit the content to max 100 words
        
        Slide Six:
        1. This slide is category description page in tabular form
        2. In this slide we need some tabular data based on user query
        3. This is the sample Category Description for User Query `SpaceTech Industry`:
        `
            | Category | Description |
            | :---- | :---- |
            | **Spacecraft and Satellites** | Vehicles and devices designed for space missions, including communication, observation, and research. |
            | **Space Vehicles** | Vehicles used for crewed and uncrewed space exploration and travel, such as space shuttles and landers. |
            | **Orbital Launch Vehicles** | Rockets designed to carry payloads into Earth's orbit or beyond, including reusable rockets. |
            | **Deep-Space Communication** | Technologies and systems enabling communication with spacecraft over long distances, essential for exploration. |
            | **In-Space Propulsion** | Propulsion systems designed for maneuvering and travel within space, including ion thrusters and chemical rockets. |
            | **Space Habitats** | Structures designed for human habitation in space, such as space stations and lunar bases. |
            | **Specialized Manufacturing Processes** | Advanced manufacturing techniques, including 3D printing and microgravity production, tailored for space applications. | 
        `
        
        4. The above sample explain the exact format of the required category description table.
        
        Slide Seven: 
        1. This slide is application page in tabular form
        2. In this slide we need some tabular data based on user query
        3. This is the sample application for User Query `SpaceTech Industry`:
        `
            **Applications**

            | Category | Description |
            | :---- | :---- |
            | **Commercial** | Includes satellite services (e.g., communication, internet), space tourism, and in-space manufacturing. |
            | **Defense and Military** | National security applications, such as surveillance, communication, and missile defense systems. |
            | **Scientific Research** | Focuses on space exploration, data collection, and advancing our understanding of the universe. |
            | **Navigation and Positioning** | Involves GPS and other satellite-based systems critical for transportation, logistics, and geolocation. |
        `
        
        4. The above sample explain the exact format of the required application table.
        
        Slide Eight:
        1. This slide is end users page in tabular form
        2. In this slide we need some tabular data based on user query
        3. This is the sample end users for User Query `SpaceTech Industry`:
        `
            **End Users**

            | Category | Description |
            | :---- | :---- |
            | **Government** | Includes space agencies (e.g., NASA, ESA) and defense departments leveraging space technologies for exploration and national security. |
            | **Commercial Enterprises** | Private space companies and satellite operators providing services like communication, internet, and Earth observation. |
            | **Research and Educational Institutions** | Universities and research organizations focusing on scientific studies, technology development, and space exploration projects. |
            | **Others** | Non-profit organizations and international collaborations promoting research, space sustainability, and global partnerships. |           
        `
        
        4. The above sample explain the exact format of the required end users table.
        """
        
        # system_prompt2=f"""
        # You are a PowerPoint Presentation Generator
        # You are assigned with a part of ppt generation
        # You will be writing the content for 2 slides of ppt 
        # All our output text will be in markdown
        
        
        # """
        
        user_prompt1=f"""
        Give me the Market Size & Structure of {prompt}
        """
        
        # user_prompt2=f"""
        # Give me the application of {prompt}
        # """
        
        # response1 = client1.chat.create(
        #     model="pplx-70b-chat", 
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": system_prompt1
        #         },
        #         {
        #             "role": "user",
        #             "content": user_prompt1
        #         }
        #     ],
        #     response_format={
        #     "type": "json_schema",
        #     "json_schema": {
        #         "name": "application_slides",
        #         "schema": {
        #             "type": "object",
        #             "properties": {
        #                 "slide_1_application_table": { "type": "string" },
        #                 "slide_2_end_users_table": { "type": "string" },
                        
        #             },
        #             "required": ["slide_1_application_table", "slide_2_end_users_table"],
        #             "additionalProperties": False,
        #         },
        #         "strict": True,
        #     },
        # },
        # )
        
        response2 = client2.chat.completions.create(
             model="gpt-4o-mini",
           messages=[
                {
                    "role":"system",
                    "content":system_prompt1
                },
                {
                    "role": "user",
                    "content": user_prompt1
                }
            ],
           response_format={
               "type":"json_schema",
               "json_schema":{
                   "name": "market_slides",
                   "schema":{
                       "type": "object",
                       "properties": {
                           "slide_1_overview_paragraph": {
                               "type": "string"
                           },
                           "slide_2_sector_wise_key_activities_table": { "type": "string" },
                           "slide_3_major_segment":{
                               "type": "string"
                           },
                           "slide_4_market_segment_table":{
                               "type": "string"
                           },
                           "slide_5_core_technology":{
                               "type": "string"
                           },
                           "slide_6_category_description":{
                               "type": "string"
                           },
                           "slide_7_application_table":{
                               "type": "string"
                           },
                           "slide_8_end_users_table":{
                               "type": "string"
                           }
                       },
                       "required":["slide_1_overview_paragraph","slide_2_sector_wise_key_activities_table","slide_3_major_segment","slide_4_market_segment_table","slide_5_core_technology","slide_6_category_description","slide_7_application_table","slide_8_end_users_table"],
                       "additionalProperties": False,
                   },
                   "strict": True,
               }
           }
        )
        
        data = json.loads(response2.choices[0].message.content)
        
        print(data["slide_1_overview_paragraph"])
        print(data["slide_2_sector_wise_key_activities_table"])
        print(data["slide_3_major_segment"])
        print(data["slide_4_market_segment_table"])
        print(data["slide_5_core_technology"])
        print(data["slide_6_category_description"])
        print(data["slide_7_application_table"])
        print(data["slide_8_end_users_table"])
        
       
        # perplexity_data = json.loads(response1.choices[0].message.content)
        # openai_data = json.loads(response2.choices[0].message.content)
        
        # combined_data = {
        # "slide_1_overview_paragraph": openai_data["slide_1_overview_paragraph"],
        # "slide_2_sector_wise_key_activities_table": openai_data["slide_2_sector_wise_key_activities_table"],
        # "slide_3_major_segment": openai_data["slide_3_major_segment"],
        # "slide_4_market_segment_table": openai_data["slide_4_market_segment_table"],
        # "slide_5_core_technology": openai_data["slide_5_core_technology"],
        # "slide_6_category_description": openai_data["slide_6_category_description"],
        # "slide_7_application_table": perplexity_data["slide_1_application_table"],
        # "slide_8_end_users_table": perplexity_data["slide_2_end_users_table"]
    # }
        
        # print(combined_data)
        