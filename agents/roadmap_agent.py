import google.generativeai as genai

def generate_roadmap(df, api_key):

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    prompt = f"""
You are a sustainability strategist.

Dataset:
{df.to_string()}

Create a realistic Net-Zero roadmap.

Provide:

1. Current emissions
2. 5-year reduction targets
3. Key reduction initiatives
4. ESG recommendations

Keep concise.
"""

    response = model.generate_content(prompt)

    return response.text
