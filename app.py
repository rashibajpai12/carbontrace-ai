import streamlit as st
from agents.simulator_agent import simulate_reduction
from agents.root_cause_agent import analyze_root_cause
from agents.roadmap_agent import generate_roadmap
import pandas as pd
import plotly.express as px

from agents.emission_agent import calculate_emissions
from agents.hotspot_agent import identify_hotspots
from agents.leak_agent import detect_leaks
from agents.recommendation_agent import generate_recommendations

st.set_page_config(
    page_title="CarbonTrace AI",
    page_icon="🌱",
    layout="wide"
)

st.title("CarbonTrace AI")
st.subheader(
    "Agentic Carbon Intelligence System"
)

df = pd.read_csv(
    "carbon_activity_data.csv"
)

df = calculate_emissions(df)

st.metric(
    "Total Carbon Emissions",
    f"{df['total_emission'].sum():,.0f} kg CO₂e"
)

hotspots = identify_hotspots(df)

st.markdown("## Carbon Hotspots")

st.bar_chart(hotspots)

leaks = detect_leaks(df)

st.markdown("## Carbon Leakage Detection")

st.dataframe(
    leaks,
    use_container_width=True
)

api_key = st.secrets.get(
    "GEMINI_API_KEY"
)

if st.button("Analyze Carbon Leakage"):

    result = analyze_root_cause(df)

    st.markdown("## Root Cause Analysis")

    st.write(
        f"Highest emitter: {result['department']}"
    )

    st.write(
        f"Contribution: {result['contribution']}%"
    )

    st.write(
        f"Emission Source: {result['driver']}"
    )
    st.markdown("## What-If Carbon Reduction Simulator")

activity_choice = st.selectbox(
    "Select activity to reduce",
    df["activity_type"].unique()
)

reduction_percent = st.slider(
    "Reduction percentage",
    0,
    100,
    25
)

simulation = simulate_reduction(
    df,
    activity_choice,
    reduction_percent
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Current Activity Emissions",
    f"{simulation['current_emission']:,.0f} kg CO₂e"
)

c2.metric(
    "Emissions Saved",
    f"{simulation['saved_emission']:,.0f} kg CO₂e"
)

c3.metric(
    "Total Projected Emissions",
    f"{simulation['total_projected']:,.0f} kg CO₂e"
)

st.success(
    f"Reducing {activity_choice} by {reduction_percent}% can reduce total emissions by {simulation['saving_percent']}%."
)

if st.button("Generate ESG Recommendations"):

    report = generate_recommendations(
        df,
        api_key
    )

    st.markdown("## ESG Recommendations")

    st.write(report)

    report = generate_recommendations(
        df,
        api_key
    )

    st.markdown(report)
