import google.generativeai as genai


def generate_recommendations(df, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    total_emissions = df["total_emission"].sum()

    dept_emissions = (
        df.groupby("department")["total_emission"]
        .sum()
        .sort_values(ascending=False)
    )

    activity_emissions = (
        df.groupby("activity_type")["total_emission"]
        .sum()
        .sort_values(ascending=False)
    )

    highest_dept = dept_emissions.index[0]
    highest_dept_emission = dept_emissions.iloc[0]

    highest_activity = activity_emissions.index[0]
    highest_activity_emission = activity_emissions.iloc[0]

    contribution_percent = (
        highest_dept_emission / total_emissions
    ) * 100

    reduction_percent = 25
    potential_reduction = highest_dept_emission * 0.25
    projected_emission = highest_dept_emission - potential_reduction

    if contribution_percent >= 70:
        risk_level = "Critical"
    elif contribution_percent >= 45:
        risk_level = "High"
    elif contribution_percent >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    prompt = f"""
You are CarbonTrace AI, a sustainability intelligence agent.

Generate a professional ESG carbon intelligence report using ONLY the numbers below.

Company Carbon Summary:
Total emissions: {total_emissions:.2f} kg CO2e

Highest emitting department:
{highest_dept}

Highest department emissions:
{highest_dept_emission:.2f} kg CO2e

Highest emitting activity:
{highest_activity}

Highest activity emissions:
{highest_activity_emission:.2f} kg CO2e

Contribution of highest department:
{contribution_percent:.2f}%

Carbon risk level:
{risk_level}

Reduction scenario:
Reduce emissions from {highest_dept} by {reduction_percent}%

Potential reduction:
{potential_reduction:.2f} kg CO2e

Projected emissions after reduction:
{projected_emission:.2f} kg CO2e

Generate the report in this structure:

1. Executive Summary
2. Carbon Risk Level
3. Evidence from Data
4. Quantified Reduction Potential
5. 90-Day Action Plan
6. Net-Zero Recommendation

Rules:
- Be specific.
- Use the exact numbers provided.
- Avoid generic advice.
- Keep it business-ready.
"""

    response = model.generate_content(prompt)

    return response.text
