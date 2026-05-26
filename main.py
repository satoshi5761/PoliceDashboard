import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LAPD Crime Intelligence",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@300;400;500&display=swap');

html, body { margin: 0; padding: 0; }
[data-testid="stAppViewContainer"]  { background: #070b12 !important; }
[data-testid="stMain"]              { background: #070b12 !important; }
.block-container                    { padding: 0.6rem 1.4rem 0 !important; max-width:100% !important; }
header[data-testid="stHeader"]      { display: none !important; }
[data-testid="stToolbar"]           { display: none !important; }
footer                              { display: none !important; }

[data-testid="stSidebar"]           { background: #0a0f1c !important; border-right: 1px solid #172030; }
[data-testid="stSidebar"] *         { color: #7a96b4 !important; font-family: 'IBM Plex Mono', monospace; font-size: 11px; }
[data-testid="stSidebar"] h3        { color: #c8d8ea !important; font-family: 'Rajdhani', sans-serif !important; font-size: 15px !important; letter-spacing: 2.5px; text-transform: uppercase; }
[data-testid="stSidebar"] .stMarkdown hr { border-color: #172030; }

[data-testid="stTabs"] > div:first-child { border-bottom: 1px solid #172030; margin-bottom: 0; }
button[data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3d5a7a !important;
    padding: 8px 20px !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #3d9eff !important;
    border-bottom: 2px solid #3d9eff !important;
}
[data-testid="stTabsContent"] { padding-top: 10px !important; }

.kpi {
    background: #0D1726;
    border: 1px solid #1A2A3A;
    border-radius: 6px;
    padding: 10px 14px;
    box-shadow: 0 0 12px rgba(0,0,0,.25);
}
.kpi-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 1.8px;
    text-transform: uppercase; color: #344d66;
    margin-bottom: 4px;
}
.kpi-val { color: #E6EEF8; font-size: 26px; font-weight: 700; font-family: 'Rajdhani', sans-serif; line-height: 1.1; }
.kpi-val.sm { font-size: 17px; line-height: 1.3; }
.kpi-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; color: #2e4a66; margin-top: 3px;
}
.up   { color: #ff4455 !important; }
.down { color: #00e676 !important; }

.dh-wrap {
    display: flex; align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #172030;
    padding-bottom: 8px; margin-bottom: 10px;
}
.dh-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px; font-weight: 700;
    color: #ddeeff; letter-spacing: 3px;
    text-transform: uppercase;
}
.dh-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; color: #2e4a66; margin-top: 2px; letter-spacing: 1px;
}
.badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; background: #0a1220;
    border: 1px solid #172030; border-radius: 4px;
    padding: 3px 9px; color: #3d9eff; margin-left: 6px;
}
.alert {
    background: rgba(255,60,60,0.07);
    border: 1px solid rgba(255,60,60,0.25);
    border-left: 3px solid #ff3c3c;
    border-radius: 5px; padding: 7px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #ff7070;
    margin: 6px 0;
}


.priority-panel {
    background: #0D1726;
    border: 1px solid #1A2A3A;
    border-radius: 6px;
    padding: 12px;
    height: 460px;

    overflow-y: auto;
    overflow-x: hidden;

    box-sizing: border-box;
}

.priority-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #253d55;
    margin-bottom: 12px;
}

.priority-row {
    display: flex;
    align-items: center;
    gap: 5px;

    width: 100%;
    min-width: 0;

    margin-bottom: 8px;
}

.priority-rank {
    flex: 0 0 18px;

    text-align: right;

    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #253d55;
}

.priority-name {
    flex: 0 0 70px;

    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #aac4de;
}

.priority-bar-wrap {
    flex: 1 1 auto;
    min-width: 30px;

    height: 6px;

    background: #08111d;
    border-radius: 3px;

    overflow: hidden;
}

.priority-bar {
    height: 100%;
    border-radius: 3px;
}

.priority-count {
    flex: 0 0 28px;

    text-align: right;

    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #344d66;
}

.priority-badge {
    flex: 0 0 auto;

    padding: 1px 4px;

    border-radius: 3px;

    font-family: 'IBM Plex Mono', monospace;
    font-size: 7px;
    font-weight: 600;

    white-space: nowrap;
}

.priority-homicide {
    flex: 0 0 auto;

    font-family: 'IBM Plex Mono', monospace;
    font-size: 8px;

    white-space: nowrap;
}
            

[data-baseweb="tag"] {
    background: rgba(77,163,255,.15) !important;
    border: 1px solid rgba(77,163,255,.35) !important;
    color: #A8D0FF !important;
}
div[data-testid="stPlotlyChart"] { border-radius: 7px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ── CONSTANTS ─────────────────────────────────────────────────────────────────
LAPD_STATIONS = pd.DataFrame([
    {"Division": "Central",     "LAT": 34.0522, "LON": -118.2437},
    {"Division": "Rampart",     "LAT": 34.0685, "LON": -118.2743},
    {"Division": "Southwest",   "LAT": 34.0017, "LON": -118.3077},
    {"Division": "Hollenbeck",  "LAT": 34.0551, "LON": -118.2100},
    {"Division": "Harbor",      "LAT": 33.7867, "LON": -118.2923},
    {"Division": "Hollywood",   "LAT": 34.1016, "LON": -118.3383},
    {"Division": "Wilshire",    "LAT": 34.0622, "LON": -118.3497},
    {"Division": "West LA",     "LAT": 34.0489, "LON": -118.4437},
    {"Division": "Van Nuys",    "LAT": 34.1872, "LON": -118.4489},
    {"Division": "W Valley",    "LAT": 34.1953, "LON": -118.5553},
    {"Division": "Northeast",   "LAT": 34.1119, "LON": -118.2225},
    {"Division": "77th St",     "LAT": 33.9561, "LON": -118.2873},
    {"Division": "Newton",      "LAT": 34.0003, "LON": -118.2603},
    {"Division": "Pacific",     "LAT": 33.9858, "LON": -118.4528},
    {"Division": "N Hollywood", "LAT": 34.1867, "LON": -118.3869},
    {"Division": "Foothill",    "LAT": 34.2658, "LON": -118.3917},
    {"Division": "Devonshire",  "LAT": 34.2669, "LON": -118.5000},
    {"Division": "Southeast",   "LAT": 33.9414, "LON": -118.2461},
    {"Division": "Mission",     "LAT": 34.2764, "LON": -118.4578},
    {"Division": "Olympic",     "LAT": 34.0564, "LON": -118.3114},
    {"Division": "Topanga",     "LAT": 34.1831, "LON": -118.6083},
])

CRIME_COLORS = {
    "Sex Crime":     "#E056FD",
    "Robbery":       "#F5A524",
    "Assault":       "#FF7A45",
    "Burglary":      "#4DA3FF",
    "Theft":         "#00C2FF",
    "Vehicle Crime": "#52C41A",
    "Vandalism":     "#7B61FF",
    "Narcotics":     "#13C2C2",
    "Other":         "#708090",
}

BG     = "#071018"
BG2    = "#0D1726"
GRID   = "#1A2A3A"
TEXT   = "#A8B8CC"
TEXT2  = "#E6EEF8"
ACCENT = "#4DA3FF"
SUCCESS = "#2ECC71"
WARNING = "#F5A524"
DANGER  = "#FF5A5F"

BASE_LAYOUT = dict(
    paper_bgcolor=BG2, plot_bgcolor=BG2,
    font=dict(color=TEXT, family="IBM Plex Mono, monospace", size=10),
    margin=dict(l=8, r=8, t=32, b=8),
    title_font=dict(color="#aac4de", size=11, family="IBM Plex Mono, monospace"),
    legend=dict(bgcolor=BG, bordercolor=GRID, borderwidth=1,
                font=dict(color=TEXT, size=9)),
)

def chart(fig, h=240):
    fig.update_layout(**BASE_LAYOUT, height=h)
    fig.update_xaxes(gridcolor=GRID, zeroline=False, tickfont=dict(size=9))
    fig.update_yaxes(gridcolor=GRID, zeroline=False, tickfont=dict(size=9))
    return fig

# ── HELPERS ───────────────────────────────────────────────────────────────────
def categorize(desc):
    d = str(desc).upper()
    # if any(k in d for k in ["HOMICIDE","MURDER","MANSLAUGHTER"]): return "Homicide"
    if any(k in d for k in ["RAPE","SEX","LEWD","INDECENT","SODOMY","CHILD ABUSE"]): return "Sex Crime"
    if any(k in d for k in ["ROBBERY","PURSE","CARJACK"]): return "Robbery"
    if any(k in d for k in ["ASSAULT","BATTERY","BRANDISH","SHOTS"]): return "Assault"
    if any(k in d for k in ["BURGLARY"]): return "Burglary"
    if any(k in d for k in ["THEFT","STEAL","SHOPLIFTING","PICKPOCKET","BUNCO","FRAUD"]): return "Theft"
    if any(k in d for k in ["VEHICLE","AUTO","MOTORCYCLE"]): return "Vehicle Crime"
    if any(k in d for k in ["VANDAL","GRAFFITI","ARSON"]): return "Vandalism"
    if any(k in d for k in ["DRUG","NARCOTIC","MARIJUANA","COCAINE"]): return "Narcotics"
    return "Other"

def severity_color(rank, total):
    pct = rank / max(total, 1)
    if pct <= 0.20: return "#FF5A5F", "#3a0a0a"   # critical: red
    if pct <= 0.45: return "#F5A524", "#3a2200"   # high: amber
    if pct <= 0.70: return "#3d9eff", "#0a1e3a"   # moderate: blue
    return "#2e4a66", "#0a1220"                    # low: muted

@st.cache_data
def load(fname):
    df = pd.read_parquet(fname)
    df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])
    df["CRIME CATEGORY"] = df["Crm Cd Desc"].apply(categorize)
    df["HOUR"] = (df["TIME OCC"].astype(str).str.zfill(4).str[:2].astype(int)
                  if "TIME OCC" in df.columns else 12)
    df["DAY OF WEEK"] = df["DATE OCC"].dt.day_name()
    df["DATE ONLY"]   = df["DATE OCC"].dt.date
    df["ARMED"]       = df["Weapon Desc"].apply(
        lambda x: str(x).strip().upper() not in ["NO WEAPON","NAN","","NONE"])
    sex_map = {"M":"Male","F":"Female","X":"Unknown","H":"Unknown","-":"Unknown"}
    df["Vict Sex Clean"] = df["Vict Sex"].map(sex_map).fillna("Unknown")
    df["Age Group"] = pd.cut(
        df["Vict Age"].replace(0, np.nan),
        bins=[0,12,17,25,35,50,65,200],
        labels=["<12","13-17","18-25","26-35","36-50","51-65","65+"]
    )
    return df

# ── LOAD ─────────────────────────────────────────────────────────────────────
df_raw   = load("crime_sample_50k.parquet")
DATE_MAX = df_raw["DATE OCC"].max()
DATE_MIN = df_raw["DATE OCC"].min()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🚔 LAPD COMMAND")
    st.markdown(f"<div style='font-size:9px;color:#253d55;margin-bottom:12px;font-family:IBM Plex Mono'>LAST UPDATE: {DATE_MAX.strftime('%b %d, %Y').upper()}</div>", unsafe_allow_html=True)

    all_areas = sorted(df_raw["AREA NAME"].unique())
    st.markdown("**📍 DIVISION**")
    sel_area = st.multiselect("", all_areas, default=all_areas, label_visibility="collapsed")

    all_cats = sorted(df_raw["CRIME CATEGORY"].unique())
    st.markdown("**🔴 CATEGORY**")
    sel_cats = st.multiselect("", all_cats, default=all_cats, label_visibility="collapsed")

    st.markdown("**🗓️ PERIOD**")
    topt = st.radio("", ["24 H","7 D","30 D","90 D","Custom"], index=2, label_visibility="collapsed")

    if   topt == "24 H":  dfrom = DATE_MAX - pd.Timedelta(hours=24); dto = DATE_MAX
    elif topt == "7 D":   dfrom = DATE_MAX - pd.Timedelta(days=7);   dto = DATE_MAX
    elif topt == "30 D":  dfrom = DATE_MAX - pd.Timedelta(days=30);  dto = DATE_MAX
    elif topt == "90 D":  dfrom = DATE_MAX - pd.Timedelta(days=90);  dto = DATE_MAX
    else:
        dfrom = pd.Timestamp(st.date_input("From", DATE_MAX - pd.Timedelta(days=30),
                                           min_value=DATE_MIN.date(), max_value=DATE_MAX.date()))
        dto   = pd.Timestamp(st.date_input("To",   DATE_MAX.date(),
                                           min_value=DATE_MIN.date(), max_value=DATE_MAX.date()))

    st.markdown("**⚙️ MAP**")
    show_sta  = st.checkbox("Police Stations", value=True)
    color_by  = st.radio("Color by", ["Crime Type","Division"], label_visibility="visible")
    armed_only= st.checkbox("Armed only", value=False)

    st.markdown("---")
    st.caption("For authorized personnel only.")

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["AREA NAME"].isin(sel_area) &
    df_raw["CRIME CATEGORY"].isin(sel_cats) &
    (df_raw["DATE OCC"] >= dfrom) &
    (df_raw["DATE OCC"] <= dto)
].copy()
if armed_only:
    df = df[df["ARMED"]]

pdays = max((dto - dfrom).days, 1)
df_prev = df_raw[
    (df_raw["DATE OCC"] >= dfrom - pd.Timedelta(days=pdays)) &
    (df_raw["DATE OCC"] <  dfrom) &
    df_raw["AREA NAME"].isin(sel_area)
]

# ── KPIs ─────────────────────────────────────────────────────────────────────
N          = len(df)
N_prev     = len(df_prev)
delta      = N - N_prev
dpct       = (delta / N_prev * 100) if N_prev > 0 else 0
dsym       = "▲" if delta >= 0 else "▼"
dcls       = "up" if delta >= 0 else "down"
top_area   = df["AREA NAME"].value_counts().index[0]        if N else "—"
top_area_n = df["AREA NAME"].value_counts().iloc[0]         if N else 0
armed_pct  = df["ARMED"].mean() * 100                       if N else 0
homicides  = int((df["CRIME CATEGORY"] == "Homicide").sum())
daily_avg  = N / pdays

# Priority areas data
area_stats = (df.groupby("AREA NAME")
                .agg(Total=("CRIME CATEGORY","count"),
                     Homicides=("CRIME CATEGORY", lambda x: (x=="Homicide").sum()),
                     Armed=("ARMED","sum"))
                .reset_index()
                .sort_values("Total", ascending=False)
                .reset_index(drop=True))
area_max = area_stats["Total"].max() if len(area_stats) > 0 else 1

def kpi(label, value, sub, accent="#3d9eff", extra_cls=""):
    return f"""<div class="kpi">
        <div class="kpi-lbl">{label}</div>
        <div class="kpi-val {extra_cls}" style="color:{accent}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

# ── HEADER ────────────────────────────────────────────────────────────────────
plabel = f"{dfrom.strftime('%b %d')}–{dto.strftime('%b %d, %Y')}"
st.markdown(f"""<div class="dh-wrap">
  <div>
    <div class="dh-title">🚔 LAPD Crime Intelligence</div>
    <div class="dh-sub">LOS ANGELES POLICE DEPARTMENT · COMMAND CENTER · LAW ENFORCEMENT SENSITIVE</div>
  </div>
  <div>
    <span class="badge">📅 {plabel}</span>
    <span class="badge">📍 {len(sel_area)} DIV</span>
    <span class="badge">📊 {N:,} INC</span>
    <span class="badge">⚡ {daily_avg:.0f}/DAY</span>
  </div>
</div>""", unsafe_allow_html=True)

if homicides >= 5:
    st.markdown(f'<div class="alert">⚠ ALERT — {homicides} homicide(s) in selected period. Command review recommended.</div>', unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "◈  OVERVIEW",
    "◈  ANALYTICS",
    "◈  DIVISION INTEL",
])

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TAB 1 — OVERVIEW                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab1:
    # ── 4 KPI strip ──────────────────────────────────────────────────────────
    k1, k3, k4 = st.columns(3)

    k1.markdown(kpi(
        "Total Incidents", f"{N:,}",
        f'<span class="{dcls}">{dsym} {abs(delta):,} ({abs(dpct):.1f}%)</span> vs prev period',
        "#ff3d3d"
    ), unsafe_allow_html=True)


    k3.markdown(kpi(
        "Armed Incidents", f"{armed_pct:.1f}%",
        f"{int(df['ARMED'].sum()):,} incidents with weapon",
        "#bf5fff"
    ), unsafe_allow_html=True)

    k4.markdown(kpi(
        "Hotspot Division", top_area,
        f"{top_area_n:,} incidents · {(top_area_n/N*100):.1f}% of total" if N else "—",
        "#f5a524", "sm"
    ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)


    # ── Main Intelligence Map ────────────────────────────────────────────────
    st.markdown("""
    <div style="
    font-family:IBM Plex Mono;
    font-size:9px;
    letter-spacing:2px;
    text-transform:uppercase;
    color:#253d55;
    margin-bottom:6px">
    Geospatial Incident Intelligence
    </div>
    """, unsafe_allow_html=True)

    color_col = "CRIME CATEGORY" if color_by == "Crime Type" else "AREA NAME"
    cmap      = CRIME_COLORS if color_by == "Crime Type" else {}

    map_df = df.sample(min(N, 10000), random_state=42) if N > 10000 else df

    fig_map = px.scatter_map(
        map_df,
        lat="LAT",
        lon="LON",
        color=color_col,
        color_discrete_map=cmap if color_by == "Crime Type" else None,
        hover_data={
            "AREA NAME": True,
            "CRIME CATEGORY": True,
            "Crm Cd Desc": True,
            "Vict Age": True,
            "Weapon Desc": True,
            "LAT": False,
            "LON": False
        },
        map_style="carto-darkmatter",
        zoom=9,
        center={"lat": 34.0522, "lon": -118.2437},
        opacity=0.82
    )

    fig_map.update_traces(
        marker=dict(size=5)
    )

    if show_sta:
        fig_map.add_trace(
            go.Scattermap(
                lat=LAPD_STATIONS["LAT"],
                lon=LAPD_STATIONS["LON"],
                mode="markers+text",
                marker=dict(
                    size=14,
                    color="#00e5ff",
                    opacity=0.95
                ),
                text=LAPD_STATIONS["Division"],
                textposition="top center",
                textfont=dict(
                    color="#00e5ff",
                    size=8,
                    family="IBM Plex Mono"
                ),
                name="Police Station",
                hovertemplate="<b>%{text} HQ</b><extra></extra>",
            )
        )

    fig_map.update_layout(
        height=780,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor=BG,
        legend=dict(
            bgcolor=BG2,
            bordercolor=GRID,
            borderwidth=1,
            font=dict(color=TEXT, size=9),
            orientation="v",
            x=0.01,
            y=0.99,
            xanchor="left",
            yanchor="top",
        ),
    )

    st.plotly_chart(fig_map, use_container_width=True)



# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TAB 2 — ANALYTICS                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab2:
    r1a, r1b = st.columns([3, 2])

    with r1a:
        DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        heat = (df.groupby(["DAY OF WEEK","HOUR"]).size()
                  .reset_index(name="Count")
                  .pivot(index="DAY OF WEEK", columns="HOUR", values="Count")
                  .fillna(0)
                  .reindex([d for d in DAYS if d in df["DAY OF WEEK"].values]))
        fig_h = px.imshow(heat,
                         color_continuous_scale=["#0D1726","#1F4E79","#4DA3FF","#F5A524","#FF5A5F"],
                         aspect="auto", title="Crime Frequency: Hour × Day")
        chart(fig_h, h=270)
        fig_h.update_layout(coloraxis_showscale=False)
        fig_h.update_xaxes(title="Hour of Day (24h)", tickmode="linear", dtick=2)
        fig_h.update_yaxes(title="")
        st.plotly_chart(fig_h, use_container_width=True)

    with r1b:
        sx = df["Vict Sex Clean"].value_counts().reset_index()
        sx.columns = ["Sex","Count"]
        fig_sx = px.pie(sx, names="Sex", values="Count", hole=0.55,
                        color_discrete_sequence=[ACCENT,"#ff6b9d","#3d5a7a"],
                        title="Victim Sex")
        chart(fig_sx, h=270)
        fig_sx.update_traces(textinfo="percent", textfont_size=9)
        fig_sx.update_layout(showlegend=True)
        st.plotly_chart(fig_sx, use_container_width=True)

    r2a, r2b, r2c = st.columns(3)

    with r2a:
        top15 = df["Crm Cd Desc"].value_counts().head(10).reset_index()
        top15.columns = ["Crime","Count"]
        top15 = top15.sort_values("Count")
        fig_c = px.bar(top15, x="Count", y="Crime", orientation="h",
                       title="Top 10 Crime Types", color_discrete_sequence=[ACCENT])
        chart(fig_c, h=310)
        fig_c.update_yaxes(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=8))
        st.plotly_chart(fig_c, use_container_width=True)

    with r2b:
        wdf = df[df["ARMED"]]
        tw  = wdf["Weapon Desc"].value_counts().head(8).reset_index()
        tw.columns = ["Weapon","Count"]
        tw = tw.sort_values("Count")
        fig_w = px.bar(tw, x="Count", y="Weapon", orientation="h",
                       title="Top Weapons Used", color_discrete_sequence=["#ff3d3d"])
        chart(fig_w, h=310)
        fig_w.update_yaxes(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=8))
        st.plotly_chart(fig_w, use_container_width=True)

    with r2c:
        ag = (df["Age Group"].value_counts().sort_index()
                             .dropna().reset_index())
        ag.columns = ["Age Group","Count"]
        fig_ag = px.bar(ag, x="Age Group", y="Count",
                        title="Victim Age Groups",
                        color_discrete_sequence=["#f0883e"])
        chart(fig_ag, h=310)
        fig_ag.update_xaxes(gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_ag, use_container_width=True)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TAB 3 — DIVISION INTEL                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab3:
    t3a, t3b = st.columns([3, 2])

    with t3a:
        pivot = (df.groupby(["AREA NAME","CRIME CATEGORY"]).size()
                   .reset_index(name="Count")
                   .pivot(index="AREA NAME", columns="CRIME CATEGORY", values="Count")
                   .fillna(0))
        fig_mx = px.imshow(pivot, text_auto=True,
                           color_continuous_scale=[BG,"#1a2a3a","#ff3d3d"],
                           aspect="auto", title="Division × Crime Category Matrix")
        chart(fig_mx, h=460)
        fig_mx.update_layout(coloraxis_showscale=False)
        fig_mx.update_traces(textfont=dict(size=8))
        fig_mx.update_xaxes(tickfont=dict(size=9))
        fig_mx.update_yaxes(tickfont=dict(size=9))
        st.plotly_chart(fig_mx, use_container_width=True)

    with t3b:
        div_st = (df.groupby("AREA NAME")
                    .agg(Total=("CRIME CATEGORY","count"),
                         Homicides=("CRIME CATEGORY", lambda x: (x=="Homicide").sum()),
                         Armed=("ARMED","sum"),
                         Top=("CRIME CATEGORY", lambda x: x.value_counts().index[0] if len(x)>0 else "—"))
                    .reset_index()
                    .rename(columns={"AREA NAME":"Division"})
                    .sort_values("Total", ascending=False))
        div_st["Armed%"] = (div_st["Armed"]/div_st["Total"]*100).round(1).astype(str)+"%"
        div_st = div_st.drop(columns=["Armed"])

        st.markdown("<div style='font-family:IBM Plex Mono;font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:#253d55;margin-bottom:6px'>Division Breakdown</div>", unsafe_allow_html=True)
        st.dataframe(div_st, use_container_width=True, height=460,
            column_config={
                "Division":  st.column_config.TextColumn("Division"),
                "Total":     st.column_config.NumberColumn("Total", format="%d"),
                "Homicides": st.column_config.NumberColumn("Homicide", format="%d"),
                "Armed%":    st.column_config.TextColumn("Armed%"),
                "Top":       st.column_config.TextColumn("Top Crime"),
            })

    st.markdown("<div style='font-family:IBM Plex Mono;font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:#253d55;margin:10px 0 6px'>Recent Incident Log</div>", unsafe_allow_html=True)
    log_cols = [c for c in ["DATE OCC","AREA NAME","CRIME CATEGORY","Crm Cd Desc",
                             "Vict Age","Vict Sex Clean","Weapon Desc","Premis Desc"] if c in df.columns]
    st.dataframe(
        df[log_cols].sort_values("DATE OCC", ascending=False).head(300),
        use_container_width=True, height=220,
        column_config={
            "DATE OCC":       st.column_config.DatetimeColumn("Date", format="MMM DD YY"),
            "AREA NAME":      st.column_config.TextColumn("Division"),
            "CRIME CATEGORY": st.column_config.TextColumn("Category"),
            "Crm Cd Desc":    st.column_config.TextColumn("Crime"),
            "Vict Age":       st.column_config.NumberColumn("Age"),
            "Vict Sex Clean": st.column_config.TextColumn("Sex"),
            "Weapon Desc":    st.column_config.TextColumn("Weapon"),
            "Premis Desc":    st.column_config.TextColumn("Location"),
        }
    )
    st.caption(f"Showing 300 most recent · {N:,} total in selection")