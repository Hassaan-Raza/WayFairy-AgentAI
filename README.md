# 🌍 WayFairy — AI Travel Planner

> *Plan your perfect trip in minutes, not hours.*

WayFairy is a multi-agent AI travel planner built with **CrewAI**, **Streamlit**, and **Ollama**. You tell it where you're going, when, how you're getting there, and what you're into — and a crew of four specialized AI agents gets to work: researching hotels, finding hidden gems, building your packing list, and assembling a polished day-by-day itinerary. Complete with a PDF you can take offline.

---

## ✨ Features

- **Multi-agent planning** — Four dedicated AI agents work in sequence: a logistics researcher, a local guide, a packing specialist, and a master planner who synthesizes everything
- **Real web research** — Agents search the web via DuckDuckGo for actual hotel names, prices, visa rules, and local tips — not hallucinated generics
- **Live weather preview** — See current conditions at your destination before you generate the plan
- **Budget estimator** — Instant cost breakdown by accommodation, food, activities, and transport as you fill in the form
- **Multimodal transport** — Works for ✈️ plane, 🚂 train, 🚌 bus, 🚗 car, and 🚲 bike trips, with route details tailored to each
- **Smart packing list** — Weather-aware, activity-specific, and transport-specific packing lists organized by category
- **PDF export** — Download a clean, formatted travel plan PDF to use offline or share
- **Interest-matched recommendations** — Every restaurant, attraction, and activity is chosen specifically for your stated interests

---

## 🏗️ Architecture

```
app.py                  ← Streamlit UI, session state, weather & budget preview
│
├── WayFairyAgents.py   ← Four CrewAI agents (LLM config, roles, backstories)
├── WayFairyTasks.py    ← Task definitions with prompts for each agent
├── WayFairyTools.py    ← DuckDuckGo web search tool (wrapped for CrewAI)
└── pdf_gen.py          ← FPDF2-based PDF renderer for the final travel plan
```

### The Agent Crew

| Agent | Role | Tools |
|---|---|---|
| 🗺️ **Location Expert** | Hotels, visa info, transport routes, local logistics | Web search |
| 🏙️ **Guide Expert** | Attractions, restaurants, day trips, local tips | Web search |
| 🧳 **Packing Specialist** | Categorized, trip-specific packing list | None (uses context) |
| 📋 **Master Planner** | Day-by-day itinerary + budget synthesis | None (uses context) |

Agents run **sequentially** — the Planner only synthesizes what the first two agents actually found, keeping the output grounded and coherent.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An [Ollama Cloud](https://ollama.com) API key
- (Optional) A `.env` file or Streamlit `secrets.toml` for credentials

### Installation

```bash
git clone https://github.com/your-username/wayfairy.git
cd wayfairy
pip install -r requirements.txt
```

### Configuration

Create a `.streamlit/secrets.toml` file:

```toml
OLLAMA_API_KEY = "your-ollama-api-key"
OLLAMA_MODEL   = "gemma4:31b-cloud"   # default — change to any supported model
```

Or set them as environment variables:

```bash
export OLLAMA_API_KEY=your-ollama-api-key
export OLLAMA_MODEL=gemma4:31b-cloud
```

### Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🖥️ Usage

1. **Enter your trip details** — departure city, destination, dates, transport mode, and daily budget
2. **Describe your interests** — e.g. *"street food, architecture, local markets, coffee shops"*
3. **Check the live preview** — weather and a rough budget estimate appear automatically
4. **Hit Generate** — agents run for 2–4 minutes (real web searches happen here)
5. **Explore your plan** — three tabs: Travel Plan, Packing List, Budget Breakdown
6. **Download** — export as a PDF or markdown file

---

## 📦 Dependencies

```
streamlit          — UI framework
crewai             — Multi-agent orchestration
crewai-tools       — Tool wrappers for CrewAI
langchain-community — DuckDuckGo search integration
duckduckgo-search  — Web search backend
ollama             — LLM client
fpdf2              — PDF generation
litellm            — LLM provider abstraction
```

Install everything with:

```bash
pip install -r requirements.txt
```

---

## 📁 Output Files

During a run, WayFairy writes intermediate agent outputs to disk:

| File | Contents |
|---|---|
| `city_report.md` | Location expert findings (hotels, transport, visa, tips) |
| `guide_report.md` | Guide expert findings (attractions, restaurants, day trips) |
| `packing_list.md` | Packing specialist output |
| `travel_plan.md` | Final synthesized itinerary from the Master Planner |

These are cleared automatically at the start of each new run.

---

## 🎨 Design

WayFairy uses a warm travel-editorial aesthetic:

- **Playfair Display** for headings — editorial serif
- **DM Sans** for body — clean and readable
- **DM Mono** for labels and metadata — precise and structured
- Color palette: sand `#F5F0E8`, ocean `#1A6B8A`, gold `#C9A84C`, ink `#1A1A2E`

---

## 🔧 Customization

**Swap the LLM** — change `OLLAMA_MODEL` in secrets to any model available on Ollama Cloud. The agents are model-agnostic.

**Adjust agent behavior** — edit roles, goals, backstories, and `max_iter` in `WayFairyAgents.py`.

**Change the itinerary structure** — the planner prompt template lives in `WayFairyTasks.py` → `planner_task()`. Every section header and output format is controlled there.

**Modify the PDF layout** — `pdf_gen.py` handles all rendering logic. Colors, fonts, and section styles are easy to tweak.

---

## ⚠️ Notes

- Generation takes **2–4 minutes** — agents make multiple real web searches
- Results quality depends on the LLM and web search results; prices are estimates and labeled as such
- The app disables CrewAI's knowledge storage (`CREWAI_KNOWLEDGE_DISABLED=True`) to avoid conflicts in stateless deployments

---

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT

---

<div align="center">
  <sub>Made with ❤️ by <strong>Hassaan Raza</strong> · Powered by CrewAI · Ollama Cloud · DuckDuckGo</sub>
</div>
