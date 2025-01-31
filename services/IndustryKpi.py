from openai import OpenAI
import json

client= OpenAI()

class IndustryKpiService:
    
    def generate_tabular(prompt: str="EV"):
        system_prompt= f"""
        You are a Powerpoint Presentation Generator
        You are assigned with a part of ppt generation
        You will be writing the content for 1 slides of ppt
        All our output text will be in markdown

        Ensure that the markdown is correctly formatted with all gaps and layout, including line breaks. 
        All tables and charts must be displayed correctly, and all headings and their subheadings should be accurate.
        
        Slide One:
        1. This slide is Industry KPIs page in tabular form
        2. In this slide we need some tabular data based on user query
        3. This is the sample Industry KPIs for User Query `SpachTech Industry`:
        `
        | Category | KPI | Description |
        | :---- | :---- | :---- |
        | Financial KPIs | Revenue Growth | Annual increase in revenue from space-related products and services. |
        |  | Cost Per Launch | Tracks cost efficiency of satellite launches, especially for reusable rockets and small satellites. |
        |  | R\&D Spending as % of Revenue | Measures investment in innovation and technology development. |
        |  | Profit Margin | Assesses profitability by comparing revenue to operational costs. |
        |  | Funding Secured | Tracks capital raised through private equity, government grants, or public offerings. |
        | Operational KPIs | Successful Mission Rate | Percentage of successful satellite launches or missions. |
        |  | Time to Market | Duration from project inception to deployment. |
        |  | Payload Utilization Efficiency | Optimization of payload capacity in launch vehicles. |
        |  | Satellite Uptime | Monitors the reliability of deployed satellites. |
        |  | Turnaround Time for Reusable Rockets | Time required to refurbish and relaunch reusable rockets. |
        | Technological KPIs | Innovation Rate | Number of patents, technological breakthroughs, or new products annually. |
        |  | Data Processing Speed | Efficiency in collecting, processing, and delivering satellite data to end-users. |
        |  | Propulsion Efficiency | Monitors advancements in fuel efficiency and sustainability for propulsion systems. |
        |  | Orbital Accuracy | Precision in satellite deployment and positioning. |
        | Customer and Market KPIs | Customer Acquisition Rate | Growth of commercial clients, such as telecom companies or government contracts. |
        |  | Market Share | Measures the company’s share in specific SpaceTech sectors. |
        |  | Customer Satisfaction Score (CSAT) | Reflects client satisfaction with services like satellite data or launch reliability. |
        |  | Service Latency | Time taken to deliver data or services to end-users. |
        | Sustainability and Risk KPIs | Space Debris Mitigation Compliance | Adherence to debris mitigation guidelines. |
        |  | Environmental Impact Score | Evaluates the ecological footprint of launches and operations. |
        |  | Cybersecurity Incident Rate | Tracks frequency of cyber threats or breaches in space systems. |
        |  | Mission Risk Assessment | Evaluates likelihood and impact of mission failures. |
        | Growth and Expansion KPIs | Global Presence | Tracks expansion into new markets or regions. |
        |  | Number of Partnerships | Measures collaborations with government agencies, private enterprises, or research institutions. |
        |  | New Product Launches | Reflects introduction of innovative solutions or services in the market. |
        |  | Market Penetration Rate | Assesses success in gaining traction in existing or emerging markets. |
        `
        
       4. The above sample explain the exact format of the required Industry KPIs table.
       5. Start with main title as "# Industry KPIs" for complete slides. 
        """
        
        user_prompt = f"""
        Give me the Industy KPIs table for {prompt}
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
                "type":"json_schema",
                "json_schema":{
                    "name": "industry_kpi_slides",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "industry_kpi_slide_1_industry_kpi_table":{ "type" : "string"}
                        },
                        "required" : ["industry_kpi_slide_1_industry_kpi_table"],
                        "additionalProperties": False,
                    },
                    "strict":True,
                },
            },
        )
        
        data = json.loads(response.choices[0].message.content)
        
        print(data["industry_kpi_slide_1_industry_kpi_table"]);

        return data