# A-IMPACT: Business Licensing Compliance Assistant

## 📌 Introduction
**A-IMPACT** is an AI-powered compliance assistant designed to help small business owners in Israel navigate the complex process of business licensing.  

The system takes raw regulatory documents (PDF/Word), transforms them into structured, machine-readable data, and then uses this knowledge to generate **personalized compliance reports in Hebrew**.  

Business owners provide their profile information (e.g., business size, seating capacity, use of gas, food type, deliveries), and the system automatically matches their data with relevant regulations. The result is a clear, concise, and actionable report that highlights the exact requirements they must follow.

This project demonstrates:
- **Data extraction and structuring** from unstructured regulatory documents.  
- **Rule matching** between regulatory frameworks and real business profiles.  
- **Interactive questionnaire** for collecting business details.  
- **LLM-powered reporting** that produces professional, easy-to-read compliance reports.  
- **End-to-end pipeline** integrating backend APIs, frontend UI, and AI agents.  

---

## 🚀 Key Features

- **Automated Data Extraction**  
  Converts raw regulatory documents (PDF/Word) into structured JSON format.  

- **Business Profile Questionnaire**  
  Collects essential information such as business size, seating capacity, use of gas, food type, and delivery options.  

- **Smart Rule Matching**  
  Matches the business profile against compiled regulatory requirements to identify exactly which rules apply.  

- **Personalized Compliance Reports**  
  Generates professional Hebrew-language reports with clear explanations and actionable next steps.  

- **End-to-End Pipeline**  
  Orchestrates the entire workflow from raw documents → structured data → rule matching → report generation.  

- **Modular Architecture**  
  Built with FastAPI, a simple frontend (HTML/JS), and modular Python scripts for maintainability.  

- **Testing & Validation**  
  Comprehensive unit and integration tests ensure correctness of each stage, from extraction to reporting.  

---

## 🏗️ System Architecture

The A-IMPACT system is built as a modular pipeline with clear separation between data processing, business logic, and user interaction.

A-IMPACT/
├── backend/                     # FastAPI backend
│   ├── main.py                  # Entry point for the backend API
│   ├── config.py                # Configuration settings
│   ├── routes/                  # API routes
│   │   ├── questionnaire.py
│   │   └── report.py
│   ├── models/                  # Pydantic models
│   │   └── user_input.py
│   ├── core/                    # Core business logic
│   │   ├── matcher.py
│   │   ├── matcher_from_regdoc.py
│   │   ├── regulation_parser.py
│   │   ├── report_generator.py
│   │   └── full_pipeline.py
│   ├── utils/                   # Utility modules
│   │   ├── llm_client.py
│   │   └── logging_config.py
│   ├── scripts/                 # Data processing scripts
│   │   ├── extract_regulations.py
│   │   ├── build_regulations_json.py
│   │   ├── compile_rules_from_regdoc.py
│   │   └── run_match_example.py
│   ├── prompts/                 # LLM prompt templates
│   │   └── report_prompt.yaml
│   └── tests/                   # Unit & integration tests
│       ├── conftest.py
│       ├── test_extract_regulations.py
│       ├── test_matcher.py
│       ├── test_questionnaire_api.py
│       ├── test_report_generator.py
│       ├── test_endpoints.py
│       ├── test_llm_client_google.py
│       └── test_llm_client_ollama.py
│
├── frontend/                    # Simple HTML/JS frontend
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── data/                        # Input & output data
│   ├── rew/                     # Raw regulatory documents
│   │   ├── 18-07-2022_4.2A.docx
│   │   └── 18-07-2022_4.2A.pdf
│   ├── processed/               # Processed regulations (JSON)
│   ├── matches/                 # Business-specific matched rules
│   └── report/                  # Final compliance reports
│
├── docs/                        # Documentation & diagrams
│   └── architecture.png
│
├── .env.example
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── ARCHITECTURE.txt
└── משימה.md


### High-Level Flow
1. **Frontend** – Simple HTML/JS interface for collecting business information and displaying reports.  
2. **Backend (FastAPI)** – API routes for questionnaire and report generation, orchestrating pipeline stages.  
3. **Core Pipeline** – Extracts regulations, matches rules, and generates compliance reports.  
4. **Data Layer** – Stores raw documents (`data/rew/`), processed JSON (`data/processed/`), matches (`data/matches/`), and final reports (`data/report/`).  
5. **LLM Integration** – Connects to OpenAI, HuggingFace, or Ollama using `llm_client.py` with structured prompts.  

---

## 🔄 Implementation Stages

### **Stage 1 – Data Extraction & Structuring**
- **Goal**: Convert raw regulatory documents (PDF/Word) into structured JSON rules.  
- **Key Files**:  
  - `scripts/extract_regulations.py`  
  - `scripts/build_regulations_json.py`  
  - `scripts/compile_rules_from_regdoc.py`  

---

### **Stage 2 – Questionnaire API**
- **Goal**: Collect business information from the user in a structured format.  
- **Key Files**:  
  - `routes/questionnaire.py`  
  - `models/user_input.py`  
  - `frontend/index.html`, `frontend/script.js`  

---

### **Stage 3 – Rule Matching**
- **Goal**: Match business profiles against regulatory rules.  
- **Key Files**:  
  - `core/matcher.py`  
  - `core/matcher_from_regdoc.py`  

---

### **Stage 4 – Compliance Report Generation**
- **Goal**: Generate personalized Hebrew compliance reports.  
- **Key Files**:  
  - `core/report_generator.py`  
  - `prompts/report_prompt.yaml`  

---

### **Stage 5 – Full Pipeline Orchestration**
- **Goal**: Automate the entire process end-to-end.  
- **Key Files**:  
  - `core/full_pipeline.py`  

---

### **Stage 6 – Testing & Validation**
- **Goal**: Ensure correctness and reliability across all stages.  
- **Key Files**:  
  - `tests/test_extract_regulations.py`  
  - `tests/test_matcher.py`  
  - `tests/test_report_generator.py`  
  - `tests/test_questionnaire_api.py`  
  - `tests/test_endpoints.py`  
  - `tests/test_llm_client_google.py`  
  - `tests/test_llm_client_ollama.py`  

---

## 📂 Data Directories

The `data/` folder is organized into several subdirectories, each with a specific role in the pipeline:

- **`data/rew/`**  
  - Location for **raw regulatory documents** (DOCX, PDF).  
  - Example:  
    - `18-07-2022_4.2A.docx`  
    - `18-07-2022_4.2A.pdf`  
  - These are the original documents provided by regulators.

- **`data/processed/`**  
  - Contains **processed regulations in JSON format**.  
  - Created by running `build_regulations_json.py` and `compile_rules_from_regdoc.py`.  
  - Represents structured rules extracted from the raw documents.  
  - Example:  
    - `compiled_rules.json`  

- **`data/matches/`**  
  - Contains **business-specific rule matches**.  
  - Generated when a user submits their profile and the system runs the matching step (`matcher.py`).  
  - Example:  
    - `match_restaurant_eyal.json`  

- **`data/report/`**  
  - Contains the **final compliance reports** generated for businesses.  
  - Each report combines profile data, matched rules, and LLM-based explanations.  
  - Example:  
    - `report_restaurant_eyal.md`  
    - `report_restaurant_eyal.pdf`  

---

📌 **Summary of Flow:**  
1. Place raw regulatory docs in `data/rew/`.  
2. Process them into JSON rules in `data/processed/`.  
3. Run matching → results saved in `data/matches/`.  
4. Generate final compliance reports in `data/report/`.  

## ⚙️ Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/your-username/A-IMPACT.git
cd A-IMPACT

### 2. Create virtual environment and install dependencies

python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt


###3. Configure environment
cp .env.example .env
Edit .env and set your credentials:
OPENAI_API_KEY=...
HUGGINGFACE_API_KEY=...
GOOGLE_API_KEY=...
OLLAMA_HOST=http://localhost:11434

4. Run the FastAPI backend
uvicorn backend.main:app --reload
By default, the API will be available at:
👉 http://127.0.0.1:8000

5. Open the frontend
Open the file frontend/index.html directly in your browser.
Alternatively, if you serve the frontend via FastAPI, you can access it at:
👉 http://127.0.0.1:8000/frontend/index.html
The page provides a form where you can submit a business profile and generate a compliance report.


**Tech Stack**: Python, FastAPI, LangChain, LLM APIs (OpenAI/Gemini/HuggingFace/Ollama), HTML/JS frontend
