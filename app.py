import streamlit as st
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

if st.button(
    "Generate ESG Recommendations"
):

    report = generate_recommendations(
        df,
        api_key
    )

    st.markdown(report)
