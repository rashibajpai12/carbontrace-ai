def generate_recommendations(df, api_key=None):
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

    report = f"""
# CarbonTrace AI – ESG Carbon Intelligence Report

## 1. Executive Summary
The highest carbon risk is concentrated in the **{highest_dept}** department, which contributes **{contribution_percent:.2f}%** of total emissions.

## 2. Carbon Risk Level
**Risk Level:** {risk_level}

Total company emissions are **{total_emissions:.2f} kg CO2e**.  
The highest emitting department, **{highest_dept}**, produces **{highest_dept_emission:.2f} kg CO2e**.

## 3. Evidence from Data
- Highest emitting department: **{highest_dept}**
- Department emissions: **{highest_dept_emission:.2f} kg CO2e**
- Highest emitting activity: **{highest_activity}**
- Activity emissions: **{highest_activity_emission:.2f} kg CO2e**
- Contribution to total emissions: **{contribution_percent:.2f}%**

## 4. Quantified Reduction Potential
A **25% reduction** in emissions from **{highest_dept}** can reduce emissions by approximately **{potential_reduction:.2f} kg CO2e**.

Projected department emissions after reduction: **{projected_emission:.2f} kg CO2e**.

## 5. 90-Day Action Plan
- Prioritize emission reduction in **{highest_dept}**.
- Target the main emission driver: **{highest_activity}**.
- Set a 25% reduction target for the highest-emission department.
- Review operational policies linked to the highest-emission activity.
- Track weekly progress using department-wise carbon metrics.

## 6. Net-Zero Recommendation
Start with the highest-emission department before expanding reduction plans across other departments. This creates the fastest measurable reduction and improves near-term ESG performance.
"""

    return report
