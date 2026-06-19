import google.generativeai as genai

def generate_recommendations(df, api_key):

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    prompt = f"""
You are a carbon intelligence agent.

Dataset:
{df.to_string()}

Identify:

1. Largest carbon hotspot
2. Carbon leakage source
3. Reduction opportunities
4. ESG action plan

Keep concise.
"""

    response = model.generate_content(
        prompt
    )

    return response.text
