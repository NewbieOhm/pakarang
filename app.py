import streamlit as st
import pandas as pd
import pydeck as pdk

# --------------------
# Page config (เหมือนเว็บจริง)
# --------------------
st.set_page_config(
    page_title="ReefRevive Dashboard",
    layout="wide"
)

# --------------------
# Load data
# --------------------
df = pd.read_csv("ข้อมูลจากการทำนายโดยระบบ.csv")

# --------------------
# Sidebar (เหมือนเว็บ)
# --------------------
st.sidebar.title("🌊 ReefRevive Controls")

year_selected = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].unique())
)

resilience_filter = st.sidebar.multiselect(
    "Resilience Level",
    sorted(df["predicted_resilience_level"].unique()),
    default=sorted(df["predicted_resilience_level"].unique())
)

filtered_df = df[
    (df["year"] == year_selected) &
    (df["predicted_resilience_level"].isin(resilience_filter))
]

# --------------------
# Color mapping
# --------------------
COLOR_MAP = {
    1: [215, 48, 39],
    2: [252, 141, 89],
    3: [254, 224, 139],
    4: [145, 207, 96],
    5: [26, 152, 80],
}

filtered_df["color"] = filtered_df["predicted_resilience_level"].map(COLOR_MAP)

# --------------------
# Layout (เหมือนเว็บ dashboard)
# --------------------
col1, col2 = st.columns([3, 1])

# --------------------
# Map section
# --------------------
with col1:
    st.subheader("🗺️ Spatial Coral Resilience Map")

    layer = pdk.Layer(
        "ScatterplotLayer",
        filtered_df,
        get_position='[longitude, latitude]',
        get_fill_color='color',
        get_radius=300,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=9.5,
        longitude=98.5,
        zoom=6,
        pitch=0,
    )

    tooltip = {
        "html": """
        <b>Resilience Level:</b> {predicted_resilience_level}<br/>
        <b>Confidence:</b> {confidence_score}%<br/>
        <b>Primary Driver:</b> {primary_risk_driver}<br/>
        <b>SST:</b> {sst} °C<br/>
        <b>DHW:</b> {dhw}
        """,
        "style": {"backgroundColor": "black", "color": "white"}
    }

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip
        )
    )

# --------------------
# Strategic Insight Panel (Figure 3)
# --------------------
with col2:
    st.subheader("📊 Strategic Insight")

    high_res = filtered_df[filtered_df["predicted_resilience_level"] >= 4]
    low_res = filtered_df[filtered_df["predicted_resilience_level"] <= 2]

    st.markdown("### ✅ Areas to Project")
    st.write(f"{len(high_res)} sites identified as high resilience")

    st.markdown("### ⚠️ Areas to Intervene")
    st.write(f"{len(low_res)} sites identified as high risk")

    st.markdown("---")
    st.caption("Explainable AI-driven decision support for coral restoration")

