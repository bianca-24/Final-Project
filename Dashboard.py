import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESG Insight",
    page_icon="🌿",
    layout="wide",
)

st.markdown("""
    <style>
        :root { color-scheme: light; }
    </style>
""", unsafe_allow_html=True)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #f5f5ec;
    }
    .main { background-color: #f5f5ec; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #2d5016; }

    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        color: #2d5016;
        margin-bottom: 0;
    }
    .hero-sub {
        color: #6b7c5a;
        font-size: 1rem;
        margin-top: 0.2rem;
    }
    .score-card {
        background: #2d5016;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        color: white;
    }
    .score-card .label {
        font-size: 0.85rem;
        opacity: 0.75;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .score-card .score {
        font-size: 2.8rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .score-card .grade {
        font-size: 1rem;
        opacity: 0.85;
    }
    .summary-box {
        background: #e8f0df;
        border-left: 4px solid #2d5016;
        border-radius: 8px;
        padding: 16px 20px;
        color: #2d5016;
        font-size: 0.95rem;
    }
    .stSelectbox > div > div {
        border-color: #1a73e8 !important;
    }
    .stSelectbox > div > div:focus-within {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 2px #1a73e8 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #f5f5ec !important;
    }
    [data-testid="stHeader"] {
        background-color: #f5f5ec !important;
    }
    color-scheme: light !important;
    
    [data-testid="stAppViewContainer"], 
    [data-testid="stAppViewContainer"] * {
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdownContainer"] p {
        color: #1a1a1a !important;
    }
    .stSelectbox > div > div {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    h1, h2, h3, h4 {
        color: #2d5016 !important;
    }
    [data-testid="stDataFrame"] {
        color: #1a1a1a !important;
    }
    
    [data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    
    .js-plotly-plot .plotly .gtitle,
    .js-plotly-plot .plotly text {
        fill: #1a1a1a !important;
    }
    
    [data-testid="stDataFrame"] > div {
        background-color: #ffffff !important;
    }
    iframe {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    [data-testid="stTextInput"] input,
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextInput"] input:active {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 2px #1a73e8 !important;
        outline: none !important;
    }
    
    [data-testid="stTextInput"] > div > div {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 2px #1a73e8 !important;
    }
    [data-testid="stTextInput"] > div > div:focus-within {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 2px #1a73e8 !important;
    }
    
    .js-plotly-plot .plotly .hoverlayer {
        display: none !important;
    }
    
</style>
""", unsafe_allow_html=True)

# ── Database connection ───────────────────────────────────────────────────────
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@st.cache_data
def get_companies():
    conn = get_connection()
    df = pd.read_sql("SELECT id, name, sector, country FROM companies ORDER BY name", conn)
    return df

@st.cache_data
def get_years(company_id):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT DISTINCT EXTRACT(YEAR FROM f.filing_date)::int AS year
        FROM filings f
        WHERE f.company_id = %s
        ORDER BY year DESC
    """, conn, params=(company_id,))
    return df["year"].tolist()

@st.cache_data
def get_esg_scores(company_id, year):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT e.pillar, e.score, e.summary
        FROM esg_scores e
        JOIN filings f ON e.filing_id = f.id
        WHERE f.company_id = %s
          AND EXTRACT(YEAR FROM f.filing_date) = %s
    """, conn, params=(company_id, year))
    return df

@st.cache_data
def get_historical_scores(company_id):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT EXTRACT(YEAR FROM f.filing_date)::int AS year,
               e.pillar, AVG(e.score) AS score
        FROM esg_scores e
        JOIN filings f ON e.filing_id = f.id
        WHERE f.company_id = %s
        GROUP BY year, e.pillar
        ORDER BY year
    """, conn, params=(company_id,))
    return df

@st.cache_data
def get_industry_average(year):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT e.pillar, AVG(e.score) AS score
        FROM esg_scores e
        JOIN filings f ON e.filing_id = f.id
        WHERE EXTRACT(YEAR FROM f.filing_date) = %s
        GROUP BY e.pillar
    """, conn, params=(year,))
    return df

@st.cache_data
def get_rankings(year):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT c.name AS "Company", c.sector AS "Sector", c.country AS "Country",
               ROUND(AVG(e.score)::numeric, 1) AS "ESG Score",
               ROUND(AVG(CASE WHEN e.pillar = 'E' THEN e.score END)::numeric, 1) AS "Environment",
               ROUND(AVG(CASE WHEN e.pillar = 'S' THEN e.score END)::numeric, 1) AS "Social",
               ROUND(AVG(CASE WHEN e.pillar = 'G' THEN e.score END)::numeric, 1) AS "Governance"
        FROM esg_scores e
        JOIN filings f ON e.filing_id = f.id
        JOIN companies c ON f.company_id = c.id
        WHERE EXTRACT(YEAR FROM f.filing_date) = %s
        GROUP BY c.name, c.sector, c.country
        ORDER BY "ESG Score" DESC
    """, conn, params=(year,))
    return df

@st.cache_data
def get_evidence(company_id, year):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT e.pillar, e.evidence_quote, e.justification
        FROM esg_scores e
        JOIN filings f ON e.filing_id = f.id
        WHERE f.company_id = %s
          AND EXTRACT(YEAR FROM f.filing_date) = %s
          AND e.evidence_quote IS NOT NULL
    """, conn, params=(company_id, year))
    return df

def get_grade(score):
    if score is None: return "N/A"
    if score >= 90: return "A+"
    elif score >= 80: return "A"
    elif score >= 70: return "B+"
    elif score >= 60: return "B"
    elif score >= 50: return "C+"
    else: return "C"

def get_card_color(score):
    if score is None: return "#888888"
    if score >= 8: return "#2d5016"
    elif score >= 6: return "#6b9e45"
    elif score >= 4: return "#d4891a"
    else: return "#c0392b"

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🌿 ESG Insight</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Data-driven ESG intelligence from SEC filings and annual reports</p>', unsafe_allow_html=True)
st.divider()

# ── Load companies ────────────────────────────────────────────────────────────
try:
    companies_df = get_companies()
except Exception as e:
    st.error(f"Could not connect to database: {e}")
    st.stop()

company_names = companies_df["name"].tolist()

# ── Search & Year ─────────────────────────────────────────────────────────────
col_search, col_year = st.columns([3, 1])
with col_search:
    selected_name = st.selectbox("Search for a company", company_names)

selected_row = companies_df[companies_df["name"] == selected_name].iloc[0]
company_id = selected_row["id"]

years = get_years(int(company_id))
with col_year:
    if years:
        selected_year = st.selectbox("Year", years)
    else:
        st.warning("No filings found.")
        st.stop()

# ── Company info ──────────────────────────────────────────────────────────────
st.markdown(f"### {selected_name}")
st.markdown(f"*{selected_row['sector']} · {selected_row['country']}*")
st.divider()

# ── Get scores ────────────────────────────────────────────────────────────────
scores_df = get_esg_scores(int(company_id), int(selected_year))

def get_pillar_score(pillar):
    row = scores_df[scores_df["pillar"] == pillar]
    if row.empty: return None
    return round(row["score"].mean(), 1)

e_score = get_pillar_score("E")
s_score = get_pillar_score("S")
g_score = get_pillar_score("G")

valid = [s for s in [e_score, s_score, g_score] if s is not None]
overall = round(sum(valid) / len(valid), 1) if valid else None

# ── Score Cards ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
for col, label, val in [
    (c1, "Overall ESG", overall),
    (c2, "Environment", e_score),
    (c3, "Social", s_score),
    (c4, "Governance", g_score),
]:
    color = get_card_color(val)
    display = val if val is not None else "N/A"
    with col:
        st.markdown(f"""
        <div class="score-card" style="background:{color}">
            <div class="label">{label}</div>
            <div class="score">{display}</div>
            <div class="grade">{get_grade(val)}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
col_radar, col_trend = st.columns(2)

with col_radar:
    st.markdown("#### ESG Radar")
    if e_score and s_score and g_score:
        categories = ["Environment", "Social", "Governance"]
        values_radar = [e_score, s_score, g_score]
        # close the shape
        categories += [categories[0]]
        values_radar += [values_radar[0]]

        fig_radar = go.Figure(go.Scatterpolar(
            r=values_radar,
            theta=categories,
            fill='toself',
            fillcolor='rgba(74, 124, 47, 0.3)',
            line=dict(color='#2d5016', width=2),
            marker=dict(size=7, color='#2d5016'),
        ))
        fig_radar.update_layout(
            polar=dict(
    radialaxis=dict(visible=True, range=[0, 10]),
    angularaxis=dict(gridcolor="#c0c0c0"),
    gridshape='linear',
    bgcolor="rgba(0,0,0,0)",
),
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=40, l=40, r=40),
            height=320,
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("No score data available.")

with col_trend:
    st.markdown("#### Company vs Industry Average")
    avg_df = get_industry_average(int(selected_year))

    def get_avg(pillar):
        row = avg_df[avg_df["pillar"] == pillar]
        if row.empty: return None
        return round(row["score"].mean(), 1)

    e_avg = get_avg("E")
    s_avg = get_avg("S")
    g_avg = get_avg("G")

    if e_score and s_score and g_score:
        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(
            name=selected_name,
            x=["Environment", "Social", "Governance"],
            y=[e_score, s_score, g_score],
            marker_color="#2d5016",
        ))
        fig_compare.add_trace(go.Bar(
            name="Industry Average",
            x=["Environment", "Social", "Governance"],
            y=[e_avg, s_avg, g_avg],
            marker_color="#8fbe6a",
        ))
        fig_compare.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=20, b=20, l=20, r=20),
            height=320,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            yaxis=dict(range=[0, 10], gridcolor="#e0e0d0"),
            xaxis=dict(gridcolor="#e0e0d0"),
        )
        st.plotly_chart(fig_compare, use_container_width=True)
    else:
        st.info("No data available.")

# ── Summary ───────────────────────────────────────────────────────────────────
st.markdown("#### Sentiment Summary")
summary_rows = scores_df[scores_df["summary"].notna()]
if not summary_rows.empty:
    summary = summary_rows.iloc[0]["summary"]
    st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
else:
    st.info("No summary available.")

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# ── Rankings ──────────────────────────────────────────────────────────────────
st.markdown("#### ESG Company Rankings")
sectors = ["All"] + sorted(companies_df["sector"].dropna().unique().tolist())
selected_sector = st.selectbox("Filter by Sector", sectors)
search_company = st.text_input("Search company in rankings", "")

rankings_df = get_rankings(int(selected_year))
if selected_sector != "All":
    rankings_df = rankings_df[rankings_df["Sector"] == selected_sector]
if search_company:
    rankings_df = rankings_df[rankings_df["Company"].str.contains(search_company, case=False, na=False)]

if not rankings_df.empty:
    rankings_df = rankings_df.round(1)
    rankings_df.insert(0, "Rank", range(1, len(rankings_df) + 1))
    
    # Convert to HTML with forced styling
    html_table = rankings_df.to_html(index=False)
    st.markdown(f"""
    <div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">
        <style>
            .rankings-table {{
                width: 100%;
                border-collapse: collapse;
                background-color: #ffffff;
                color: #1a1a1a;
                font-family: 'DM Sans', sans-serif;
            }}
            .rankings-table th {{
                background-color: #2d5016;
                color: white;
                padding: 8px 12px;
                text-align: left;
                font-size: 0.85rem;
            }}
            .rankings-table td {{
                padding: 8px 12px;
                border-bottom: 1px solid #e0e0d0;
                color: #1a1a1a;
                background-color: #ffffff;
                font-size: 0.85rem;
            }}
            .rankings-table tr:hover td {{
                background-color: #f0f5e9;
            }}
        </style>
        {html_table.replace('<table', '<table class="rankings-table"')}
    </div>
    """, unsafe_allow_html=True)

# ── Evidence Quotes ───────────────────────────────────────────────────────────
st.markdown("#### Evidence from Report")
evidence_df = get_evidence(int(company_id), int(selected_year))

if not evidence_df.empty:
    tab_e, tab_s, tab_g = st.tabs(["Environment", "Social", "Governance"])
    for tab, pillar in [(tab_e, "E"), (tab_s, "S"), (tab_g, "G")]:
        with tab:
            rows = evidence_df[evidence_df["pillar"] == pillar]
            if rows.empty:
                st.info("No evidence available.")
            else:
                for _, row in rows.iterrows():
                    st.markdown(f"""
                    <div class="summary-box" style="margin-bottom:10px;">
                        <b>Justification:</b> {row['justification']}<br><br>
                        <i>"{row['evidence_quote']}"</i>
                    </div>
                    """, unsafe_allow_html=True)
else:
    st.info("No evidence available.")