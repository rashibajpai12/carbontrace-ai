import google.generativeai as genai

def generate_recommendations(df, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are CarbonTrace AI, an ESG carbon intelligence agent.

Dataset:
{df.to_string()}

Generate:
1. Main carbon finding
2. Carbon leakage source
3. Evidence from data
4. Reduction recommendation
5. ESG action plan
"""

    response = model.generate_content(prompt)
    return response.text
