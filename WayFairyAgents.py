import os
import streamlit as st
from crewai import Agent, LLM
from WayFairyTools import search_web_tool
from dotenv import load_dotenv
load_dotenv()

os.environ["CREWAI_KNOWLEDGE_DISABLED"] = "True"
os.environ["CREWAI_KNOWLEDGE_STORAGE_DISABLED"] = "True"

# ── LLM setup — Ollama Cloud ──────────────────────────────────
OLLAMA_API_KEY = st.secrets["OLLAMA_API_KEY"]
OLLAMA_MODEL   = st.secrets.get("OLLAMA_MODEL", "gemma4:31b-cloud")

llm = LLM(
    model=f"openai/{OLLAMA_MODEL}",
    api_key=OLLAMA_API_KEY,
    base_url="https://ollama.com/v1",   # <-- this was wrong before
    temperature=0.7,
)



# ── Agent 1: Location Expert ──────────────────────────────────
location_expert = Agent(
    role="Travel Logistics Expert",
    goal=(
        "Research practical travel information for the destination: "
        "hotels with real prices, visa requirements, local transport options, "
        "and flight or route details from the origin city."
    ),
    backstory=(
        "You are a seasoned travel researcher with 15 years of experience. "
        "You always find real, specific information — actual hotel names, "
        "actual price ranges, actual visa rules. You never make things up. "
        "If you cannot find exact prices, you give realistic estimates based "
        "on your knowledge and clearly label them as estimates."
    ),
    tools=[search_web_tool],
    verbose=True,
    max_iter=8,
    llm=llm,
    allow_delegation=False
)

# ── Agent 2: Guide Expert ─────────────────────────────────────
guide_expert = Agent(
    role="Local City Guide Expert",
    goal=(
        "Create a detailed, personalized activity guide for the destination "
        "based on the traveler's specific interests. Find real restaurants, "
        "real attractions, real experiences — with opening hours and prices."
    ),
    backstory=(
        "You are a passionate local guide who knows every corner of the cities "
        "you cover. You match recommendations precisely to the traveler's stated "
        "interests. You give specific names, addresses, and insider tips — not "
        "generic tourist advice. You always explain WHY each recommendation "
        "suits this particular traveler."
    ),
    tools=[search_web_tool],
    verbose=True,
    max_iter=8,
    llm=llm,
    allow_delegation=False
)

# ── Agent 3: Packing List Expert ─────────────────────────────
packing_expert = Agent(
    role="Travel Packing Specialist",
    goal=(
        "Create a smart, complete packing list based on the destination, "
        "travel dates, weather conditions, activities planned, and transport mode."
    ),
    backstory=(
        "You are a minimalist travel packer who has travelled to over 80 countries. "
        "You know exactly what to bring and what to leave behind. "
        "Your packing lists are practical, organised by category, and tailored "
        "to the specific trip — not a generic checklist."
    ),
    tools=[],
    verbose=True,
    max_iter=5,
    llm=llm,
    allow_delegation=False
)

# ── Agent 4: Planner Expert ───────────────────────────────────
planner_expert = Agent(
    role="Master Travel Planner",
    goal=(
        "Synthesise all research from the location and guide experts into "
        "a beautiful, complete, day-by-day travel plan with daily budgets, "
        "transport details, and a trip summary."
    ),
    backstory=(
        "You are a professional travel planner who turns raw research into "
        "polished, actionable itineraries. You organise everything clearly: "
        "morning, afternoon, and evening activities; transport between each; "
        "estimated daily costs; and practical tips. "
        "You NEVER search the web — you only use the context provided by "
        "the other experts. You write in an engaging, friendly tone that "
        "makes the traveler excited for their trip."
    ),
    tools=[],
    verbose=True,
    max_iter=8,
    llm=llm,
    allow_delegation=False
)