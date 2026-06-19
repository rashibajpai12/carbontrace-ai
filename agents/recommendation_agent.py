import google.generativeai as genai

def generate_recommendations(df, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    total_emissions = df["total_emission"].sum()
    top_department = (
        df.groupby("department")["total_emission"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
        .to_string()
    )
    top_activity = (
        df.groupby("activity_type")["total_emission"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
        .to_string()
    )

    prompt = f"""
You are CarbonTrace AI, an ESG carbon intelligence agent.

Carbon summary:
Total emissions: {total_emissions:.2f} kg CO2e

Highest emitting department:
{top_department}

Highest emitting activity:
{top_activity}

Generate:
1. Main carbon finding
2. Carbon leakage source
3. Evidence from the data
4. Reduction recommendation
5. ESG action plan

Keep it concise and business-ready.
"""

    response = model.generate_content(prompt)
    return response.text
