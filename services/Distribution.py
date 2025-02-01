from openai import OpenAI
import json

client = OpenAI()

class DistributionService:
    
    def get_paragraph(prompt: str="EV"):
        
        system_prompt = f"""
        You are a Powerpoint Presentation Generator
        You are assigned with a part of ppt generation
        You will be writing the content for 3 slides of ppt
        All our output text will be in markdown

        Ensure that the markdown is correctly formatted with all gaps and layout, including line breaks. 
        All tables and charts must be displayed correctly, and all headings and their subheadings should be accurate.
        
        Slide One:
        1. This slide is about end customers in SpaceTech Industry
        2. In this page we need to write paragraphs about end customers
        3. This is the sample End Customers content for Distribution:
        `
        End customers in the SpaceTech industry, including government agencies, military organizations, and commercial enterprises, leverage space technologies for diverse and impactful applications. Government agencies, such as NASA and ISRO, utilize these technologies for space exploration, scientific research, public services like meteorology and disaster management, and economic development through national space programs. Military organizations rely on satellite systems for surveillance, secure communications, missile defense, and navigation to enhance national security and precision in defense operations. Commercial enterprises drive innovation and market growth by providing satellite communication services, Earth observation data for agriculture and urban planning, space tourism experiences, and in-space manufacturing of advanced materials.

        | Category | Description |
        | :---- | :---- |
        | **Government Agencies** | End users of space technologies for exploration, research, public services, and regulatory purposes. |
        | **Military Organizations** | Rely on space systems for defense applications, including secure communication, surveillance, and reconnaissance. |
        | **Commercial Enterprises** | Use space-based technologies for commercial purposes such as satellite communication, internet services, and remote sensing. |
        `
        4. The above sample explains the exact format of the required end customers content.
        5. Start with main title as "# Distribution in (Industry_Name)" for complete slides. 
        6. Start the "### End Customers" as a heading (###) to this Slide.
        7. Limit the content to max 200 words
        
        Slide Two:
        1. This slide is about distribution models and partners
        2. In this slide we need content about distribution models and partners
        3. This is the sample Distribution Models and Partners content:
        `
        ### Key Distribution Models

        SpaceTech distribution models have evolved significantly to address the challenges of handling and delivering massive amounts of data generated by space technologies. The industry has seen a shift towards more efficient and secure distribution methods to meet the growing demand for space-derived information.

        | Distribution Model | Description |
        | :---- | :---- |
        | **Cloud-Based Platforms** | Cloud computing enables efficient storage, processing, and delivery of large volumes of SpaceTech data. Example: Amazon's platform for the Landsat program. |
        | **Direct Satellite Access** | Offers secure and immediate access to satellite data, mainly for international government clients, crucial for military and national security. |
        | **Reseller Networks** | Utilizes dedicated reseller networks to effectively access local markets, ensuring tailored services for specific regions or industries. |
        | **Online Data Archives** | Hosts satellite data archives on company websites, providing users with direct access to historical and current space-derived information. |

        ### Distribution Partners

        | Distribution Channel | Description |
        | :---- | :---- |
        | **Reseller Networks** | Dedicated networks used by SpaceTech companies to effectively access and serve local markets. |
        | **Cloud Service Providers** | Companies like Amazon Web Services (AWS) offer cloud-based platforms to handle and deliver massive space-derived data. |
        | **Government Agencies** | Organizations such as NASA and ESA collaborate with private companies to distribute space technologies and capabilities. |
        | **Satellite Operators** | Companies like Thales Alenia Space, Viasat, and Siminn work with solution providers to distribute satellite-based services. |
        `
        4. The above sample explains the exact format of the required distribution models and partners content.
        
        Slide Three:
        1. This slide is about emerging channels
        2. In this slide we need content about emerging distribution channels
        3. This is the sample Emerging Channels content:
        `
        ### Emerging Channels

        | Category | Description |
        | :---- | :---- |
        | **Cloud-Based Platforms** | Essential for handling and distributing massive space-derived data, such as the 3 terabytes per day produced by Copernicus Sentinel-1. |
        | **Data Brokering Services** | Emerging actors collect, process, and sell space-derived data to other organizations, creating new opportunities in the value chain. |
        | **Internet of Things (IoT) Integration** | Connects space-based data with ground-based devices and systems, enabling comprehensive IoT solutions. |
        | **Software-as-a-Service (SaaS) Platforms** | Companies like Quindar offer SaaS solutions for satellite mission management, improving payload operations and automating workflows. |
        | **Commercial Space Services** | Private companies like SpaceX, Blue Origin, and Virgin Galactic provide new channels for satellite launches, space exploration, and tourism. |
        | **Small Satellite Constellations** | Miniaturized satellites and small constellations reduce entry barriers and create new opportunities for space-based services. |
        | **Digital Supply Chain Platforms** | Platforms like Satsearch streamline the space industry supply chain, connecting buyers and sellers of space technology products. |
        `
        4. The above sample explains the exact format of the required emerging channels content.
        """
        
        user_prompt = f"""
        Give me the distribution content for {prompt}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using the latest GPT-4 model
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
                    "name": "distribution_slides",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "distribution_slide_1_end_customers": { "type": "string" },
                            "distribution_slide_2_distribution_models_and_partners": { "type": "string" },
                            "distribution_slide_3_emerging_channels": { "type": "string" },
                        },
                        "required": ["distribution_slide_1_end_customers", "distribution_slide_2_distribution_models_and_partners", "distribution_slide_3_emerging_channels"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
        )
        
        data = json.loads(response.choices[0].message.content)
        
        # print(data["distribution_slide_1_end_customers"])
        # print(data["distribution_slide_2_distribution_models_and_partners"])
        # print(data["distribution_slide_3_emerging_channels"])
        
        return data