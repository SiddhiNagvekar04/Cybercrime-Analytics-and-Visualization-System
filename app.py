
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

DETAIL_PATH = DATA_DIR / "maharashtra_cybercrime_2023_clean.csv"
SUMMARY_PATH = DATA_DIR / "maharashtra_cybercrime_2023_summary.csv"

st.set_page_config(
    page_title="CAVS | Cybercrime Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# 2. LIGHT PINK AND LAVENDER THEME
# --------------------------------------------------

st.markdown("""
<style>
/* Overall application */
.stApp {
    background: linear-gradient(
        135deg,
        #fffafd 0%,
        #fff5f9 55%,
        #fbf7ff 100%
    );
    color: #482653;
    font-family: "Segoe UI", sans-serif;
}

/* Main page spacing */
.block-container {
    max-width: 1550px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #492354 !important;
    font-weight: 700 !important;
}

p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: #61466c;
}

/* Hero header */
.hero {
    background: linear-gradient(
        110deg,
        #fff0f7 0%,
        #f9e9ff 55%,
        #fff8fc 100%
    );
    border: 1px solid #f5d5e8;
    border-radius: 24px;
    padding: 30px 34px;
    margin-bottom: 24px;
    box-shadow: 0 8px 28px rgba(155, 91, 145, 0.07);
}

.hero-title {
    color: #482052;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0;
}

.hero-subtitle {
    color: #795183;
    font-size: 17px;
    font-weight: 600;
    margin-top: 5px;
}

.hero-description {
    color: #65486e;
    font-size: 14px;
    margin-top: 15px;
    margin-bottom: 0;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid #f4d6e7;
    border-radius: 18px;
    padding: 20px 20px;
    min-height: 112px;
    box-shadow: 0 5px 18px rgba(176, 100, 154, 0.07);
}

[data-testid="stMetricLabel"] {
    color: #684573 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #482052 !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #9b4f87 !important;
}

/* Chart and content panels */
.panel {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid #f3d8e8;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 5px 18px rgba(176, 100, 154, 0.045);
}

/* Inputs */
.stTextInput input {
    background: #fff5fa !important;
    color: #482052 !important;
    border: 1px solid #efc9df !important;
    border-radius: 12px !important;
}

.stTextInput input:focus {
    border-color: #d85c9f !important;
    box-shadow: 0 0 0 1px #d85c9f !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] {
    color: #df579c;
}

/* Buttons */
.stDownloadButton button,
.stButton button {
    background: #df579c;
    color: white;
    border: none;
    border-radius: 11px;
    font-weight: 600;
    padding: 8px 18px;
}

.stDownloadButton button:hover,
.stButton button:hover {
    background: #c84187;
    color: white;
}

/* Tables */
[data-testid="stDataFrame"] {
    background: white;
    border: 1px solid #f3d8e8;
    border-radius: 14px;
    overflow: hidden;
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid #f3d8e8;
    border-radius: 14px;
}

/* Information boxes */
[data-testid="stAlert"] {
    background: #fff1f8;
    border: 1px solid #f0cce0;
    border-radius: 12px;
    color: #482052;
}

/* Horizontal dividers */
hr {
    border-color: #f2d9e8 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #fff4fa;
}

/* Footer */
.footer {
    text-align: center;
    color: #92769a;
    font-size: 12px;
    padding: 22px 0 4px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. LOAD DATASET
# --------------------------------------------------

@st.cache_data
def load_data():
    detail = pd.read_csv(DETAIL_PATH)
    summary = pd.read_csv(SUMMARY_PATH)

    detail["Cases"] = (
        pd.to_numeric(detail["Cases"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    summary["Cases"] = (
        pd.to_numeric(summary["Cases"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    detail["Crime Category"] = (
        detail["Crime Category"]
        .fillna("Unspecified")
        .astype(str)
    )

    summary["Category"] = summary["Category"].fillna("").astype(str)

    return detail, summary


try:
    df, summary = load_data()

except Exception as exc:
    st.error(
        "Unable to load the project datasets. Please check that both CSV "
        "files are available in the data folder."
    )
    st.code(str(exc))
    st.stop()


# --------------------------------------------------
# 4. HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">🛡️ CAVS</div>
    <div class="hero-subtitle">
        Cybercrime Analytics and Visualization System
    </div>
    <div style="color:#896493; font-size:13px; margin-top:7px;">
        Maharashtra Cybercrime Analytics · NCRB Crime in India 2023
    </div>
    <div class="hero-description">
        Explore reported cybercrime cases through interactive data
        analysis and visualizations.
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 5. OFFICIAL SUMMARY METRICS
# --------------------------------------------------

total_row = summary[
    summary["Category"].str.contains(
        "Total Cyber Crimes", case=False, na=False
    )
]

it_act_row = summary[
    summary["Category"].str.contains(
        "Offences under IT Act", case=False, na=False
    )
]

ipc_row = summary[
    summary["Category"].str.contains(
        "IPC Crimes", case=False, na=False
    )
]

sll_row = summary[
    summary["Category"].str.contains(
        "SLL offences", case=False, na=False
    )
]

total_cases = (
    int(total_row["Cases"].iloc[0])
    if not total_row.empty else 8103
)

it_act = int(it_act_row["Cases"].sum())
ipc = int(ipc_row["Cases"].sum())
sll = int(sll_row["Cases"].sum())

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total cybercrime cases",
    f"{total_cases:,}"
)

c2.metric(
    "Offences under IT Act",
    f"{it_act:,}"
)

c3.metric(
    "IPC crime grouping",
    f"{ipc:,}"
)

c4.metric(
    "SLL crime grouping",
    f"{sll:,}"
)


# --------------------------------------------------
# 6. INTERACTIVE CRIME CATEGORY CHART
# --------------------------------------------------

st.divider()

left, right = st.columns(
    [1.2, 0.8],
    gap="large"
)

with left:

    st.subheader("📊 Top Reported Crime Heads")

    max_categories = max(5, min(20, len(df)))

    top_n = st.slider(
        "Number of categories to display",
        min_value=5,
        max_value=max_categories,
        value=min(10, max_categories)
    )

    top = (
        df.sort_values("Cases", ascending=False)
        .head(top_n)
        .sort_values("Cases", ascending=True)
    )

    fig = px.bar(
        top,
        x="Cases",
        y="Crime Category",
        orientation="h",
        text="Cases",
        labels={
            "Cases": "Reported cases",
            "Crime Category": ""
        },
        color="Cases",
        color_continuous_scale=[
            "#ead8ff",
            "#efa6d1",
            "#df579c"
        ]
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        textfont=dict(
            color="#482052",
            size=11
        ),
        marker_line_width=0
    )

    fig.update_layout(
        template="plotly_white",
        height=max(440, top_n * 42),
        margin=dict(l=10, r=40, t=20, b=35),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(
            family="Segoe UI, sans-serif",
            color="#583c68",
            size=11
        ),
        xaxis=dict(
            title="Number of cases",
            showgrid=True,
            gridcolor="#f4e6ef",
            zeroline=False
        ),
        yaxis=dict(
            title="",
            showgrid=False,
            automargin=True
        ),
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# 7. OFFICIAL LEGAL GROUPING CHART
# --------------------------------------------------

with right:

    st.subheader("⚖️ Official Legal Grouping")

    group_summary = summary[
        summary["Category"].str.contains(
            "Offences under IT Act|IPC Crimes|SLL offences",
            case=False,
            na=False
        )
    ].copy()

    if not group_summary.empty:

        fig2 = px.pie(
            group_summary,
            names="Category",
            values="Cases",
            hole=0.52,
            color_discrete_sequence=[
                "#c7a3f4",
                "#e75a9f",
                "#f3b8dd"
            ]
        )

        fig2.update_traces(
            textposition="inside",
            textinfo="percent",
            textfont=dict(
                color="#482052",
                size=12
            ),
            marker=dict(
                line=dict(
                    color="#ffffff",
                    width=3
                )
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Cases: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        fig2.update_layout(
            template="plotly_white",
            height=390,
            margin=dict(l=5, r=5, t=20, b=15),
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(255,255,255,0)",
            font=dict(
                family="Segoe UI, sans-serif",
                color="#583c68",
                size=11
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            )
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.info(
        "The detailed crime-head rows and official legal-group totals "
        "represent different levels of the source table. Do not sum all "
        "detailed rows to reproduce the statewide total."
    )


# --------------------------------------------------
# 8. SEARCHABLE DATA TABLE
# --------------------------------------------------

st.divider()

st.subheader("🔎 Detailed Crime Head Data")

st.write(
    "Search and explore the reported crime categories included in the dataset."
)

search = st.text_input(
    "Search by crime category",
    placeholder="Try identity theft, banking fraud, stalking..."
)

if search:
    filtered = df[
        df["Crime Category"].str.contains(
            search,
            case=False,
            na=False
        )
    ]
else:
    filtered = df.copy()

st.caption(
    f"Showing {len(filtered)} of {len(df)} detailed rows."
)

st.dataframe(
    filtered.sort_values("Cases", ascending=False),
    use_container_width=True,
    hide_index=True
)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="cavs_filtered_cybercrime_data.csv",
    mime="text/csv"
)


# --------------------------------------------------
# 9. DATASET INFORMATION
# --------------------------------------------------

with st.expander("ℹ️ About the Dataset and Limitations"):

    st.markdown("""
    **Source:** NCRB, *Crime in India 2023*, Table 9A.2, as supplied
    for this project.

    **Geographical coverage:** Maharashtra.

    **Reporting period:** Calendar year 2023.

    **Analysis:** Descriptive analysis of reported cybercrime cases,
    including official legal groupings and detailed crime heads.

    **Limitations:**
    - This dataset covers one year only.
    - It does not support year-wise trend analysis.
    - It does not provide district-level analysis in this project.
    - The dashboard does not predict future crime or establish causation.
    - Crime-head categories and official group totals should be
      interpreted according to the source table's classifications.
    """)


# --------------------------------------------------
# 10. FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    CAVS · Cybercrime Analytics and Visualization System<br>
    Academic Big Data Analytics Mini-Project · Maharashtra · 2023
</div>
""", unsafe_allow_html=True)
