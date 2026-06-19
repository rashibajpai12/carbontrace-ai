import streamlit as st
import pandas as pd
import plotly.express as px

from agents.emission_agent import calculate_emissions
from agents.hotspot_agent import identify_hotspots
from agents.leak_agent import detect_leaks
from agents.root_cause_agent import analyze_root_cause
from agents.simulator_agent import simulate_reduction
from agents.recommendation_agent import generate_recommendations

st.set_page_config(
    page_title="CarbonTrace AI",
    page_icon="🌱",
    layout="wide"
)

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #030303;
    color: #F4F4F1;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 1320px;
    padding: 1.4rem 3rem 3rem 3rem;
}

[data-testid="stSidebar"] {
    background: #050505;
    border-right: 1px solid rgba(255,255,255,0.08);
}

.side-brand {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin-bottom: 8px;
}

.side-sub {
    color: #8F8F8F;
    font-size: 14px;
    margin-bottom: 34px;
    line-height: 1.7;
}

.side-section {
    margin-top: 32px;
    margin-bottom: 14px;
    color: #777;
    font-size: 11px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
}

.side-pill {
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
    border-radius: 999px;
    padding: 11px 14px;
    margin-bottom: 10px;
    color: #D7D7D7;
    font-size: 13px;
    line-height: 1.45;
}

.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 45px;
}

.logo {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.04em;
}

.nav-links {
    display: flex;
    gap: 30px;
    color: #B8B8B8;
    font-size: 14px;
    font-weight: 600;
}

.sign-btn {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    padding: 11px 20px;
    color: #F5F5F5;
    background: rgba(255,255,255,0.04);
}

.hero {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 34px;
    align-items: center;
    min-height: 320px;
    margin-bottom: 18px;
}

.eyebrow {
    display: flex;
    align-items: center;
    gap: 16px;
    color: #747474;
    font-size: 11px;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.eyebrow-line {
    width: 32px;
    height: 1px;
    background: #787878;
}

.hero-title {
    font-size: clamp(58px, 6vw, 92px);
    font-weight: 820;
    letter-spacing: -0.07em;
    line-height: 0.94;
    max-width: 760px;
    color: #F2F2EE;
}

.hero-title span {
    color: #DDE8D8;
}

.hero-desc {
    margin-top: 28px;
    max-width: 640px;
    color: #A7ACB8;
    font-size: 18px;
    line-height: 1.65;
    font-weight: 500;
}

.hero-actions {
    display: flex;
    gap: 14px;
    margin-top: 34px;
}

.action-primary, .action-secondary {
    border-radius: 999px;
    padding: 13px 23px;
    font-size: 14px;
    font-weight: 700;
    display: inline-block;
}

.action-primary {
    border: 1px solid rgba(255,255,255,0.16);
    background: rgba(255,255,255,0.055);
    color: #F4F4F1;
}

.action-secondary {
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.025);
    color: #F4F4F1;
}

.carbon-card {
    border: 1px solid rgba(255,255,255,0.09);
    background: radial-gradient(circle at top right, rgba(210,232,210,0.12), transparent 38%),
                rgba(255,255,255,0.025);
    border-radius: 30px;
    padding: 30px;
    min-height: 300px;
    position: relative;
    overflow: hidden;
}

.carbon-title {
    color: #DDE8D8;
    font-size: 14px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 22px;
}

.control-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 18px;
}

.control-box {
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.035);
    border-radius: 18px;
    padding: 18px;
}

.control-label {
    color: #8F8F8F;
    font-size: 12px;
    margin-bottom: 10px;
}

.control-value {
    color: #F4F4F1;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.04em;
}

.tree-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(221,232,216,0.35), transparent);
    margin: 24px 0;
}

.mini-forest {
    display: flex;
    gap: 18px;
    align-items: end;
    height: 56px;
}

.mini-tree {
    width: 24px;
    height: 48px;
    position: relative;
}

.mini-tree:before {
    content: "";
    position: absolute;
    bottom: 0;
    left: 10px;
    width: 5px;
    height: 27px;
    border-radius: 10px;
    background: rgba(221,232,216,0.65);
}

.mini-tree:after {
    content: "";
    position: absolute;
    top: 0;
    left: 1px;
    width: 25px;
    height: 25px;
    border-radius: 50%;
    background: rgba(221,232,216,0.88);
    box-shadow: 13px 10px 0 rgba(221,232,216,0.68), -8px 13px 0 rgba(221,232,216,0.62);
}

.metric-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-top: 18px;
    margin-bottom: 34px;
}

.metric-card {
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
    border-radius: 22px;
    padding: 22px;
    min-height: 118px;
}

.metric-card.accent {
    background: #DDE8D8;
    color: #050505;
}

.metric-label {
    font-size: 13px;
    color: #8D8D8D;
    font-weight: 600;
}

.metric-card.accent .metric-label {
    color: #373737;
}

.metric-value {
    margin-top: 24px;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.06em;
}

.brief-card {
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 34px;
}

.brief-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.05em;
    margin-bottom: 18px;
}

.brief-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.brief-item {
    border-left: 1px solid rgba(221,232,216,0.35);
    padding-left: 16px;
}

.brief-label {
    color: #8F8F8F;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 8px;
}

.brief-value {
    color: #F4F4F1;
    font-size: 16px;
    font-weight: 700;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.035);
    border-radius: 999px;
    padding: 10px 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

div[data-testid="stAlert"] {
    border-radius: 18px;
}
</style>
""")

with st.sidebar:
    st.html("""
    <div class="side-brand">CarbonTrace <span style="color:#DDE8D8;">●</span></div>
    <div class="side-sub">Agentic carbon intelligence workspace for ESG decision support.</div>

    <div class="side-section">Carbon Agents</div>
    <div class="side-pill">Emission Calculator</div>
    <div class="side-pill">Hotspot Detector</div>
    <div class="side-pill">Carbon Leak Analyzer</div>
    <div class="side-pill">Root Cause Agent</div>
    <div class="side-pill">ESG Recommendation Agent</div>

    <div class="side-section">Focus Areas</div>
    <div class="side-pill">Business Travel</div>
    <div class="side-pill">Diesel Logistics</div>
    <div class="side-pill">Electricity Usage</div>
    <div class="side-pill">Cloud Emissions</div>
    """)

df = pd.read_csv("carbon_activity_data.csv")
df = calculate_emissions(df)

hotspots = identify_hotspots(df)
leaks = detect_leaks(df)

total_emissions = df["total_emission"].sum()
departments = df["department"].nunique()
activities = df["activity_type"].nunique()
locations = df["location"].nunique()

dept_emissions = df.groupby("department")["total_emission"].sum().sort_values(ascending=False)
highest_emitter = dept_emissions.index[0]
highest_emission = dept_emissions.iloc[0]
highest_contribution = (highest_emission / total_emissions) * 100

activity_emissions = df.groupby("activity_type")["total_emission"].sum().sort_values(ascending=False)
top_activity = activity_emissions.index[0]
top_activity_emission = activity_emissions.iloc[0]

default_reduction = 25
reduction_potential = (top_activity_emission * default_reduction / 100) / total_emissions * 100

leak_events = len(leaks)
carbon_risk_score = round(highest_contribution)

st.html("""
<div class="top-nav">
    <div class="logo">CarbonTrace ●</div>
    <div class="nav-links">
        <span>Leak Detection</span>
        <span>ESG Report</span>
        <span>Simulator</span>
        <span>Roadmap</span>
    </div>
    <div class="sign-btn">Live System</div>
</div>
""")

st.html(f"""
<div class="hero">
    <div>
        <div class="eyebrow">
            <div class="eyebrow-line"></div>
            Agentic Carbon Intelligence
        </div>

        <div class="hero-title">
            Operational Emissions, <span>Explained.</span>
        </div>

        <div class="hero-desc">
            CarbonTrace identifies emission hotspots, detects carbon leakage,
            explains root causes, and estimates reduction impact before ESG teams
            commit to sustainability actions.
        </div>

        <div class="hero-actions">
            <div class="action-primary">Analyze Carbon →</div>
            <div class="action-secondary">View ESG Workflow</div>
        </div>
    </div>

    <div class="carbon-card">
        <div class="carbon-title">Carbon Intelligence Control Center</div>

        <div class="mini-forest">
            <div class="mini-tree"></div>
            <div class="mini-tree" style="transform:scale(1.2);"></div>
            <div class="mini-tree" style="transform:scale(0.9);"></div>
            <div class="mini-tree" style="transform:scale(1.05);"></div>
        </div>

        <div class="tree-line"></div>

        <div class="control-grid">
            <div class="control-box">
                <div class="control-label">Carbon Leakage Alerts</div>
                <div class="control-value">{leak_events}</div>
            </div>

            <div class="control-box">
                <div class="control-label">Highest Emitter</div>
                <div class="control-value">{highest_emitter}</div>
            </div>

            <div class="control-box">
                <div class="control-label">Reduction Potential</div>
                <div class="control-value">{reduction_potential:.1f}%</div>
            </div>

            <div class="control-box">
                <div class="control-label">Carbon Risk Score</div>
                <div class="control-value">{carbon_risk_score}/100</div>
            </div>
        </div>
    </div>
</div>
""")

st.html(f"""
<div class="metric-strip">
    <div class="metric-card accent">
        <div class="metric-label">Total Emissions ↗</div>
        <div class="metric-value">{total_emissions:,.0f}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Highest Emitter ↗</div>
        <div class="metric-value">{highest_emitter}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Leak Events ↗</div>
        <div class="metric-value">{leak_events}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Carbon Risk Score ↗</div>
        <div class="metric-value">{carbon_risk_score}/100</div>
    </div>
</div>
""")

st.html(f"""
<div class="brief-card">
    <div class="brief-title">AI Carbon Brief</div>

    <div class="brief-grid">
        <div class="brief-item">
            <div class="brief-label">Primary Hotspot</div>
            <div class="brief-value">{highest_emitter}</div>
        </div>

        <div class="brief-item">
            <div class="brief-label">Carbon Driver</div>
            <div class="brief-value">{top_activity}</div>
        </div>

        <div class="brief-item">
            <div class="brief-label">Contribution</div>
            <div class="brief-value">{highest_contribution:.1f}% of total emissions</div>
        </div>

        <div class="brief-item">
            <div class="brief-label">Suggested Action</div>
            <div class="brief-value">Reduce {top_activity} by 25%</div>
        </div>
    </div>
</div>
""")

tab1, tab2, tab3, tab4 = st.tabs([
    "Carbon Hotspots",
    "Leak Detection",
    "Root Cause",
    "What-If Simulator"
])

with tab1:
    st.markdown("### Department-wise Carbon Hotspots")
    hotspot_df = hotspots.reset_index()
    hotspot_df.columns = ["department", "total_emission"]

    fig = px.bar(
        hotspot_df,
        x="department",
        y="total_emission",
        title="Department-wise Emissions"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#050505",
        font_color="#F4F4F1"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Carbon Leakage Detection")
    st.dataframe(leaks, use_container_width=True)

with tab3:
    st.markdown("### Root Cause Analysis")

    if st.button("Analyze Carbon Leakage"):
        result = analyze_root_cause(df)

        c1, c2, c3 = st.columns(3)

        c1.metric("Highest Emitter", result["department"])
        c2.metric("Contribution", f"{result['contribution']}%")
        c3.metric("Primary Driver", result["driver"])

with tab4:
    st.markdown("### What-If Carbon Reduction Simulator")

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
        "Projected Total Emissions",
        f"{simulation['total_projected']:,.0f} kg CO₂e"
    )

    st.success(
        f"Reducing {activity_choice} by {reduction_percent}% can reduce total emissions by {simulation['saving_percent']}%."
    )

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not configured in Streamlit Secrets.")
    st.stop()

st.markdown("## ESG Intelligence Report")

if st.button("Generate ESG Recommendations"):

    report = generate_recommendations(
        df,
        api_key
    )

    st.markdown(report)

    st.download_button(
        label="Download ESG Report",
        data=report,
        file_name="carbontrace_esg_report.txt",
        mime="text/plain"
    )
