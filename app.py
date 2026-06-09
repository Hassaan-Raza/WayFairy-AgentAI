import streamlit as st
import os
import sys
import requests
from pathlib import Path
from datetime import datetime, date

# Clean up stale output files from previous runs
for f in ["travel_plan.md", "city_report.md", "guide_report.md", "packing_list.md"]:
    if os.path.exists(f):
        os.remove(f)

os.environ["CREWAI_KNOWLEDGE_DISABLED"] = "True"
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
os.environ["CREWAI_KNOWLEDGE_STORAGE_DISABLED"] = "True"

from WayFairyAgents import location_expert, guide_expert, packing_expert, planner_expert
from WayFairyTasks import location_task, guide_task, packing_task, planner_task
from crewai import Crew, Process
from pdf_gen import generate_pdf

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="WayFairy",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Fonts ─────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
  --sky:    #E8F4FD;
  --ocean:  #1A6B8A;
  --sand:   #F5F0E8;
  --gold:   #C9A84C;
  --ink:    #1A1A2E;
  --muted:  #6B7280;
  --border: #D4CCB8;
  --cream:  #EDE8DC;
  --serif:  'Playfair Display', serif;
  --sans:   'DM Sans', sans-serif;
  --mono:   'DM Mono', monospace;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--sand) !important;
  color: var(--ink) !important;
  font-family: var(--sans) !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="collapsedControl"] { display: none !important; }

.block-container { padding: 0 !important; max-width: 100% !important; }

/* Main content wrapper — consistent side padding */
.main-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 3rem;
}

/* Force all Streamlit content to stay within padded area */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
  padding: 0 3rem;
}

/* Date input — show value properly */
[data-testid="stDateInput"] input {
  background: white !important;
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  color: var(--ink) !important;
  font-family: var(--sans) !important;
  font-size: 0.9rem !important;
  padding: 0.5rem 0.75rem !important;
  opacity: 1 !important;
}
[data-testid="stDateInput"] input:focus {
  border-color: var(--ocean) !important;
  box-shadow: 0 0 0 2px #1A6B8A22 !important;
}

/* Number input */
[data-testid="stNumberInput"] input {
  background: white !important;
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  color: var(--ink) !important;
}

.main-wrap {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
}

.stButton > button {
  background: var(--ink) !important;
  color: var(--gold) !important;
  border: 1px solid var(--gold) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  border-radius: 4px !important;
  padding: 0.6rem 1.4rem !important;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  background: var(--gold) !important;
  color: var(--ink) !important;
}

/* Download button — white bg, ocean text */
[data-testid="stDownloadButton"] > button {
  background: white !important;
  color: var(--ocean) !important;
  border: 1px solid var(--ocean) !important;
  font-size: 0.78rem !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: var(--ocean) !important;
  color: white !important;
}
[data-testid="baseButton-primary"] > button {
  background: var(--ocean) !important;
  color: white !important;
  border-color: var(--ocean) !important;
  font-size: 0.85rem !important;
  padding: 0.8rem 2rem !important;
}
[data-testid="baseButton-primary"] > button:hover {
  background: var(--ink) !important;
  border-color: var(--gold) !important;
  color: var(--gold) !important;
}

.stTextInput input, .stTextArea textarea, .stNumberInput input {
  background: white !important;
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  font-family: var(--sans) !important;
  color: var(--ink) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--ocean) !important;
  box-shadow: 0 0 0 2px #1A6B8A22 !important;
}

.stDateInput input {
  background: white !important;
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
  background: white !important;
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  color: black;
}

label { font-family: var(--mono) !important; font-size: 0.68rem !important;
        text-transform: uppercase !important; letter-spacing: 0.1em !important;
        color: var(--muted) !important; }

.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.08em !important;
  border-radius: 0 !important;
  padding: 0.6rem 1.2rem !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding: 1.5rem 2rem !important;
}

.stTabs [aria-selected="true"] {
  color: var(--ocean) !important;
  border-bottom: 2px solid var(--ocean) !important;
}

.stSpinner > div { color: var(--ocean) !important; }

hr { border-color: var(--border) !important; margin: 0 !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.weather-card {
  background: linear-gradient(135deg, #1A6B8A, #0D4A63);
  border-radius: 8px;
  padding: 1.2rem 1.5rem;
  color: white;
  font-family: var(--sans);
}
.weather-card .temp {
  font-family: var(--serif);
  font-size: 2.2rem;
  font-weight: 700;
}
.weather-card .desc {
  font-size: 0.85rem;
  opacity: 0.85;
  margin-top: 0.2rem;
}

.budget-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem 1.2rem;
  text-align: center;
}
.budget-card .label {
  font-family: var(--mono);
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted);
  margin-bottom: 0.3rem;
}
.budget-card .value {
  font-family: var(--serif);
  font-size: 1.5rem;
  color: var(--ocean);
  font-weight: 700;
}

.plan-output {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 2rem 2.5rem;
  font-family: var(--sans);
  font-size: 0.9rem;
  line-height: 1.8;
  color: var(--ink);
}

.status-bar {
  background: var(--ink);
  color: var(--gold);
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  padding: 0.6rem 1.5rem;
  border-radius: 4px;
  margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────
def get_weather(city: str) -> dict:
    """Fetch live weather from wttr.in — free, no API key needed."""
    try:
        url = f"https://wttr.in/{city.replace(' ', '+')}?format=j1"
        r = requests.get(url, timeout=8)
        data = r.json()
        current = data["current_condition"][0]
        return {
            "temp_c":   current["temp_C"],
            "temp_f":   current["temp_F"],
            "desc":     current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
            "feels_c":  current["FeelsLikeC"],
            "wind_kmph": current["windspeedKmph"],
        }
    except Exception:
        return {}


def estimate_budget(budget_per_day: int, num_days: int, transport: str) -> dict:
    """Rough budget breakdown based on daily budget and trip length."""
    total = budget_per_day * num_days
    transport_cost = {"plane": 400, "train": 150, "bus": 80, "car": 120, "bike": 30}.get(transport.lower(), 200)
    accommodation = total * 0.35
    food          = total * 0.30
    activities    = total * 0.20
    local_trans   = total * 0.10
    misc          = total * 0.05
    return {
        "total":          int(total + transport_cost),
        "transport":      transport_cost,
        "accommodation":  int(accommodation),
        "food":           int(food),
        "activities":     int(activities),
        "local_trans":    int(local_trans),
        "misc":           int(misc),
    }


# ── Session state ─────────────────────────────────────────────
for k, v in [("travel_plan", None), ("packing_list", None),
              ("weather", {}), ("budget", {}), ("generating", False)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 1.8rem 3rem 1.2rem; border-bottom: 1px solid #D4CCB8;
            display: flex; align-items: baseline; gap: 1rem;">
  <span style="font-family:'Playfair Display',serif; font-size:2.6rem; font-weight:700;
               color:#1A1A2E; letter-spacing:-0.02em;">
    Roam<span style="color:#1A6B8A; font-style:italic;">io</span>
  </span>
  <span style="font-family:'DM Mono',monospace; font-size:0.65rem; color:#6B7280;
               letter-spacing:0.15em; text-transform:uppercase;
               border:1px solid #D4CCB8; padding:2px 8px; border-radius:4px;">
    AI Travel Planner
  </span>
  <span style="font-family:'DM Mono',monospace; font-size:0.72rem; color:#6B7280;
               margin-left:auto;">
    Plan smarter. Roam further.
  </span>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Trip form ─────────────────────────────────────────────────
# Padding wrapper using CSS columns trick
_, form_col, _ = st.columns([1, 16, 1])
with form_col:

    col1, col2, col3 = st.columns([2, 2, 1], gap="large")

    with col1:
        from_city = st.text_input("Departure City", placeholder="e.g. Lahore, London, New York")
        destination_city = st.text_input("Destination City", placeholder="e.g. Istanbul, Bangkok, Paris")

    with col2:
        from datetime import timedelta
        date_from = st.date_input("Departure Date", value=date.today())
        date_to   = st.date_input("Return Date",    value=date.today() + timedelta(days=7))

    with col3:
        transport_options = {"✈️ Plane": "plane", "🚂 Train": "train",
                             "🚌 Bus": "bus", "🚗 Car": "car", "🚲 Bike": "bike"}
        transport_label = st.selectbox("Transport Mode", list(transport_options.keys()))
        transport = transport_options[transport_label]
        budget_per_day = st.number_input("Daily Budget (USD)", min_value=20, max_value=2000, value=150, step=10)

    interests = st.text_area(
        "Your Interests & Travel Style",
        placeholder="e.g. street food, architecture, hiking, nightlife, museums, local markets, adventure sports...",
        height=80
    )

st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

# ── Weather & Budget preview ──────────────────────────────────
if destination_city and destination_city != st.session_state.get("_last_city"):
    st.session_state.weather = get_weather(destination_city)
    st.session_state._last_city = destination_city

if destination_city and date_from and date_to and date_to > date_from:
    num_days = (date_to - date_from).days
    st.session_state.budget = estimate_budget(budget_per_day, num_days, transport)
else:
    st.session_state.budget = {}

if st.session_state.weather or st.session_state.budget:
    _lpad, _inner, _rpad = st.columns([1, 22, 1])
    with _inner:
        wcol, bcol1, bcol2, bcol3, bcol4 = st.columns([2, 1, 1, 1, 1], gap="medium")

        if st.session_state.weather:
            w = st.session_state.weather
            with wcol:
                st.markdown(f"""
                <div class="weather-card">
                  <div style="font-family:'DM Mono',monospace; font-size:0.62rem;
                              letter-spacing:0.1em; opacity:0.7; margin-bottom:0.3rem;">
                    CURRENT WEATHER · {destination_city.upper()}
                  </div>
                  <div class="temp">{w.get('temp_c', '?')}°C / {w.get('temp_f', '?')}°F</div>
                  <div class="desc">{w.get('desc', '')} · Feels like {w.get('feels_c', '?')}°C</div>
                  <div style="font-size:0.75rem; opacity:0.75; margin-top:0.4rem;">
                    💧 {w.get('humidity', '?')}% humidity · 💨 {w.get('wind_kmph', '?')} km/h wind
                  </div>
                </div>
                """, unsafe_allow_html=True)

        if st.session_state.budget:
            b = st.session_state.budget
            for col, label, val in [
                (bcol1, "Total Estimate",  f"${b['total']:,}"),
                (bcol2, "Accommodation",   f"${b['accommodation']:,}"),
                (bcol3, "Food & Dining",   f"${b['food']:,}"),
                (bcol4, "Activities",      f"${b['activities']:,}"),
            ]:
                with col:
                    st.markdown(f"""
                    <div class="budget-card">
                      <div class="label">{label}</div>
                      <div class="value">{val}</div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

# ── Generate button ───────────────────────────────────────────
_bl, _bc, _br = st.columns([1, 22, 1])
with _bc:
    _generate = st.button("🌍 Generate My WayFairy Plan", type="primary", use_container_width=True)

if _generate:
    if not all([from_city, destination_city, interests]):
        st.error("Please fill in departure city, destination city, and your interests.")
    elif date_to <= date_from:
        st.error("Return date must be after departure date.")
    else:
        # fetch weather for context
        weather = st.session_state.weather
        weather_summary = (
            f"{weather.get('desc', 'unknown')} at {weather.get('temp_c', '?')}°C"
            if weather else "weather data unavailable"
        )

        with st.spinner("🌍 WayFairy agents are planning your trip... This takes 2 to 4 minutes."):
            try:
                loc_task  = location_task(location_expert, from_city, destination_city,
                                          date_from, date_to, transport, budget_per_day)
                guid_task = guide_task(guide_expert, destination_city, interests,
                                       date_from, date_to, transport, budget_per_day)
                pack_task = packing_task(packing_expert, destination_city, date_from,
                                         date_to, transport, interests, weather_summary)
                plan_task = planner_task([loc_task, guid_task], planner_expert,
                                         from_city, destination_city, interests,
                                         date_from, date_to, transport, budget_per_day)

                crew = Crew(
                    agents=[location_expert, guide_expert, packing_expert, planner_expert],
                    tasks=[loc_task, guid_task, pack_task, plan_task],
                    process=Process.sequential,
                    full_output=True,
                    verbose=False,
                )

                result = crew.kickoff()
                st.session_state.travel_plan = str(result)

                # read packing list output file
                if os.path.exists("packing_list.md"):
                    with open("packing_list.md", "r", encoding="utf-8") as f:
                        st.session_state.packing_list = f.read()

                st.success("✅ Your WayFairy plan is ready!")
                st.rerun()

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────
if st.session_state.travel_plan:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="main-wrap" style="padding-top: 1rem; padding-bottom: 2rem;">', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🗺️ Travel Plan", "🧳 Packing List", "💰 Budget Breakdown"])

    with tab1:
        import re
        clean_plan = st.session_state.travel_plan
        # Prevent Streamlit from rendering bare number ranges (e.g. "20 - 40") as markdown
        clean_plan = clean_plan.replace(" - ", "–")  # prevent markdown rendering bare ranges as strikethrough
        st.markdown(clean_plan)
        try:
            pdf_data = generate_pdf(st.session_state.travel_plan, transport)
            st.download_button(
                "📄 Download Travel Plan (PDF)",
                data=pdf_data,
                file_name=f"{destination_city.replace(' ','_')}_WayFairy_Plan.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"PDF generation failed: {e}. Downloading as markdown instead.")
            st.download_button(
                "📄 Download Travel Plan",
                data=st.session_state.travel_plan,
                file_name=f"{destination_city.replace(' ','_')}_WayFairy_Plan.md",
                mime="text/markdown",
                use_container_width=True
            )

    with tab2:
        if st.session_state.packing_list:
            st.markdown(st.session_state.packing_list)
            st.download_button(
                "📄 Download Packing List",
                data=st.session_state.packing_list,
                file_name=f"{destination_city.replace(' ','_')}_Packing_List.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.info("Packing list will appear here after generating your plan.")

    with tab3:
        if st.session_state.budget:
            b = st.session_state.budget
            num_days = (date_to - date_from).days

            st.markdown(f"""
            ### 💰 Estimated Trip Budget
            *Based on ${budget_per_day}/day per person for {num_days} days*

            | Category | Estimated Cost |
            |---|---|
            | ✈️ Transport ({transport}) | ${b['transport']:,} |
            | 🏨 Accommodation | ${b['accommodation']:,} |
            | 🍽️ Food & Dining | ${b['food']:,} |
            | 🎭 Activities & Entry Fees | ${b['activities']:,} |
            | 🚇 Local Transport | ${b['local_trans']:,} |
            | 🛍️ Shopping & Misc | ${b['misc']:,} |
            | **💵 Total Estimate** | **${b['total']:,}** |

            > These are rough estimates. Actual costs vary based on your choices.
            """)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="main-wrap">
<div style="padding: 1rem 0; border-top: 1px solid #D4CCB8; margin-top: 2rem;
            display: flex; justify-content: space-between; align-items: center;">
  <span style="font-family:'DM Mono',monospace; font-size:0.62rem; color:#A09890;">
    WayFairy · AI Travel Planner · Made with ❤️ by Hassaan Raza
  </span>
  <span style="font-family:'DM Mono',monospace; font-size:0.62rem; color:#A09890;">
    Powered by CrewAI · Ollama Cloud · DuckDuckGo
  </span>
</div>
</div>
""", unsafe_allow_html=True)