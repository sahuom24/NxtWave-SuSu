# FORGE'26 GEN AI BUILDATHON — MASTER SPECIFICATION

## 1. Quick Metadata & Status
- **Event**: NxtWave Forge'26 Gen AI Buildathon (for IITs/NITs/IIITs/BITS)
- **Team Name**: SuSu (Team Code: `52XENX`)
- **Team Members**: 
  - Om (Lead, IIT Delhi - `mt1240764@iitd.ac.in`)
  - Pragya Nanhera (IIT Delhi - `mt1240674@iitd.ac.in`)
- **Time Remaining**: ~34 hours (Submission Deadline: **01 Nov, 11:59 PM IST**)
- **Prizes**: ₹2 Lakh+ cash pool + Audience Choice Award

---

## 2. Critical Compliance & Disqualification Rules (Zero Tolerance)
> ⚠️ **VIOLATING ANY OF THESE RESULTS IN IMMEDIATE DISQUALIFICATION:**
1. **NO DUMMY / MOCK DATA**:
   - Strictly prohibited: Hardcoded JSON files, static mock datasets, fake placeholder numbers.
   - **Requirement**: Must connect to an active backend consuming real-time live APIs, active databases, or real official open datasets (e.g., IMD weather API, ISRO Bhuvan, Data.gov.in, live web scrapers/APIs).
2. **GENUINE AGENTIC / AI DEPTH**:
   - Solutions must go beyond simple UI wrappers or raw `chat_completion` wrappers.
   - Must show custom pipelines (RAG, agentic tool-use loops, browser automation, state machines, geospatial models, or multi-step execution graphs).
3. **LIVE DEPLOYMENT**:
   - Must be live & deployed (e.g., Vercel, Render, Streamlit, Hugging Face Spaces).
   - Pre-recorded fake demos or mockup-only prototypes disguised as live apps are disqualified.
4. **CODE INTEGRITY**:
   - Open-source boilerplate is allowed, but all AI logic, models, agent workflows, and core functionality must be built during the hackathon window.

---

## 3. Evaluation Scoring Rubric (100 Points Total)

| Pillar | Weight | Key Assessment Criteria |
| :--- | :---: | :--- |
| **Technical Architecture & Engineering Depth** | **20 pts** | Modular codebase, low latency, custom RAG / browser automation / agent state graphs, proper API integration. |
| **AI Reasoning & Agentic Execution** | **25 pts** | Multi-step tool calling, autonomous planning, error handling/self-correction, hallucination guardrails, source attribution. |
| **Problem Relevance, Impact & USP** | **25 pts** | Genuine real-world impact, clear differentiation from off-the-shelf chatbots, novelty and scalability. |
| **Live Demonstration & Robustness** | **30 pts** | Flawless live execution without crashing, resilience against missing data/edge-case inputs. |

---

## 4. Submission Deliverables Checklist
1. **Problem Statement**: Target issue, context, affected audience.
2. **Solution Description**: High-level overview, technical architecture, models, data sources.
3. **Prototype Link**: Live hosted app URL (Vercel, Streamlit, Hugging Face, etc.).
4. **Demo Video**: 2–3 minute video link (YouTube / Loom / Drive) showing end-to-end live reasoning, tool usage, or agent execution.
5. **GitHub Repository**: Clean README, architecture diagram/flowchart, instructions, fully reproducible code.
6. **Pitch Deck**: 5–7 slides (Problem, Solution, Architecture & Innovation, Future Roadmap, Live Demo Summary).

---

## 5. Themes & Problem Tracks

### 🏛️ Theme 1: Civic Pulse, Digital Governance & Public Information
**Focus**: Democratizing information, modernizing public service delivery, fighting viral misinformation, bridging citizen-bureaucracy gaps.

- **Option 1A: Multilingual Policy, Rights & Scheme Explainer**
  - Ingests government notifications, welfare policy drafts, municipal orders.
  - Converts into regional-language plain-voice explainers with exact eligibility, step-by-step rights, and impact checks.
- **Option 1B: Transparent Civic Grievance & Infrastructure Triage System**
  - Citizens submit audio/visual reports (potholes, garbage, water leaks, damaged infrastructure).
  - Vision/Multimodal AI rates severity, extracts geolocation, classifies department, routes ticket via live API, publishes public accountability metrics.
- **Option 1C: Autonomous Public Service & Bureaucracy Execution Agent**
  - Browser-use / Playwright agent that takes user profile & intent (scholarships, subsidy, certificate renewal), navigates legacy portals, fills applications, handles UI traps, returns tracking receipt.
- **Option 1D: Real-Time Fact-Verification & Deepfake Audit Engine**
  - Multimodal verification ingestion: checks live claims/social feeds against verified registries, knowledge graphs, forensic image/audio models to trace misinformation provenance.

---

### 🌍 Theme 2: Climate, Resource Infrastructure & Global Supply Resilience
**Focus**: Extreme weather shocks, agricultural stability, resource depletion, grid/supply chain disruptions.

- **Option 2A: Multilingual Agritech & Resource Advisory Assistant**
  - Ingests live weather APIs (Open-Meteo / IMD), live mandi prices (data.gov.in / Agmarknet), soil metrics.
  - Generates actionable, crop-level advice and planting/harvesting schedules in vernacular languages.
- **Option 2B: Predictive Climate & Micro-Location Yield Engine**
  - Combines satellite feeds (Sentinel/Copernicus/ISRO open APIs), weather datasets, and soil data to predict micro-climate risks (unseasonal rain, localized drought) and output mitigation plans.
- **Option 2C: Smart Grid & Urban Resource Allocation Controller**
  - Low-latency control agent monitoring live water reserves, power micro-grids, or heatwave alerts, dynamically rebalancing resources to prevent blackouts/shortages.
- **Option 2D: Autonomous Emergency Response & Supply Chain Logistics Swarm**
  - Multi-agent swarm monitoring live extreme weather alerts & transit routes; queries regional warehouse APIs, recalculates safe delivery routes around flood/disaster zones, dispatches automated relief orders.

---

## 6. Winning Strategy & Technical Blueprint Recommendations

To win this hackathon, the solution must:
1. **Use Real Live APIs**:
   - Weather: Open-Meteo (free, no-key, real-time hourly & daily forecasts), IMD/NASA POWER APIs.
   - Civic / India Data: Data.gov.in API (mandi prices, government schemes, pin code / municipal datasets).
   - Maps / Routing: OpenStreetMap / OSRM API (free routing & geocoding).
   - LLMs / Multimodal: Google Gemini 1.5/2.0 Flash / Pro (fast, multimodal, generous free tier), or open-source Hugging Face endpoints.
2. **Feature a Real Multi-Agent / Tool-Using Engine**:
   - Implemented with LangGraph, LangChain, or lightweight custom tool-calling agents.
   - Explicit steps: *Triage/Query -> Tool Execution (API fetch) -> Guardrail Verification -> Multi-modal Output (Voice/Map/Action)*.
3. **Include a Killer Live UI**:
   - Modern Next.js/React + Tailwind or high-speed Streamlit / FastHTML with interactive Leaflet map / live dashboard.
