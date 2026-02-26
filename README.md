# Financial Document Analyzer

## Project Overview

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered multi-agent analysis. Built with **CrewAI**, **FastAPI**, and **Google Gemini**, it provides automated financial analysis, investment recommendations, and risk assessments from uploaded PDF documents.

---

## Bugs Found and How They Were Fixed

### Bug 1 — `main.py` line 6: Wrong import source for `Crew` and `Process`
**Buggy:**
```python
from crewai_tools import Crew, Process
```
**Fixed:**
```python
from crewai import Crew, Process
```
**Explanation:** `Crew` and `Process` are core CrewAI orchestration classes that belong to the `crewai` package. They do not exist in `crewai_tools`. This caused an `ImportError` on startup, preventing the application from running at all.

---

### Bug 2 — `main.py` line 48: Wrong `None`-check order
**Buggy:**
```python
if query == "" or query is None:
```
**Fixed:**
```python
if query is None or query == "":
```
**Explanation:** `query is None` must be evaluated first. In Python, if `query` is `None`, evaluating `query == ""` is safe but the logical intent requires the None guard to come first to avoid subtle bugs in edge cases where the variable might be `None` from an upstream source.

---

### Bug 3 — `tools.py` line 6: `@tool` decorator imported from wrong package
**Buggy:**
```python
from crewai_tools import tool
```
**Fixed:**
```python
from crewai import tool
```
**Explanation:** The `@tool` decorator used to create custom CrewAI tools lives in the `crewai` package, not `crewai_tools`. Importing it from `crewai_tools` raises an `ImportError`, making all custom tools (`read_data_tool`, `analyze_investment_tool`, `create_risk_assessment_tool`) unavailable.

---

### Bug 4 — `tools.py` line 7: `SerperDevTool` imported from internal submodule path
**Buggy:**
```python
from crewai_tools.tools.serper_dev_tool import SerperDevTool
```
**Fixed:**
```python
from crewai_tools import SerperDevTool
```
**Explanation:** `SerperDevTool` should be imported from the public `crewai_tools` API. The internal submodule path is an implementation detail and is not guaranteed to be stable across versions. Using the internal path can cause `ModuleNotFoundError` depending on the installed version.

---

### Bug 5 — `README.md`: Typo in install command filename
**Buggy:**
```sh
pip install -r requirement.txt
```
**Fixed:**
```sh
pip install -r requirements.txt
```
**Explanation:** The actual file is named `requirements.txt` (with an **s**). This typo causes `pip` to fail with "ERROR: Could not open requirements file: [Errno 2] No such file or directory".

---

### Bug 6 — `README.md`: Misleading debug placeholder message
**Buggy:**
```
# You're All Not Set!
🐛 Debug Mode Activated! The project has bugs...
```
**Fixed:** Removed entirely. This was a placeholder debug prompt from the assignment template, not part of the actual project documentation.

---

## Project Structure

```
financial-document-analyzer/
├── main.py            # FastAPI application and entry point
├── agents.py          # CrewAI agent definitions (analyst, verifier, advisor, risk assessor)
├── task.py            # CrewAI task definitions for each analysis stage
├── tools.py           # Custom tools (PDF reader, investment analyzer, risk assessor)
├── requirements.txt   # Python dependencies
├── .env               # API keys (GEMINI_API_KEY, SERPER_API_KEY)
├── data/
│   └── sample.pdf     # Sample financial document for testing
└── outputs/           # Analysis output storage
```

---

## Setup and Usage Instructions

### Prerequisites
- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
- A [Serper API key](https://serper.dev/) (for web search capability)

### 1. Clone the Repository
```sh
git clone https://github.com/Prasanth1830/finance-assessment.git
cd finance-assessment
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 4. Add a Sample Financial Document
Download a financial PDF (e.g., Tesla Q2 2025 Update):
```
https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
```
Save it as `data/sample.pdf` in the project directory.

### 5. Run the Application
```sh
python main.py
```
The API will start at: `http://localhost:8000`

---

## API Documentation

### `GET /`
**Health Check** — Confirms the API server is running.

**Response:**
```json
{
  "message": "Financial Document Analyzer API is running"
}
```

---

### `POST /analyze`
**Analyze a Financial Document** — Upload a PDF financial document and receive a comprehensive AI-generated analysis.

**Request (multipart/form-data):**

| Field  | Type   | Required | Description |
|--------|--------|----------|-------------|
| `file` | File   | ✅ Yes   | PDF financial document to analyze |
| `query`| String | ❌ No    | Custom analysis query (default: `"Analyze this financial document for investment insights"`) |

**Example using `curl`:**
```sh
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=What are the key investment risks?"
```

**Example using Python `requests`:**
```python
import requests

with open("data/sample.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/analyze",
        files={"file": f},
        data={"query": "Summarize revenue trends and investment outlook"}
    )

print(response.json())
```

**Success Response (200):**
```json
{
  "status": "success",
  "query": "What are the key investment risks?",
  "analysis": "## Financial Analysis Report\n...[Full multi-agent analysis output]...",
  "file_processed": "sample.pdf"
}
```

**Error Response (500):**
```json
{
  "detail": "Error processing financial document: <error message>"
}
```

---

## How It Works

The system uses a **sequential multi-agent CrewAI pipeline** with four specialized AI agents:

| Agent | Role | Tools Used |
|-------|------|-----------|
| **Document Verifier** | Validates the PDF is a real financial document, extracts company name, reporting period, and document type | PDF Reader |
| **Senior Financial Analyst** | Extracts key metrics (revenue, EPS, margins, cash flow) and performs deep financial analysis | PDF Reader, Web Search |
| **Investment Strategy Advisor** | Provides investment recommendations, valuation analysis, and growth assessment | PDF Reader, Web Search |
| **Risk Assessment Specialist** | Identifies financial, operational, market, and regulatory risks with mitigation strategies | PDF Reader, Web Search |

Each agent runs sequentially, with later agents building on earlier findings to produce a comprehensive, layered final report.

---

## Expected Output

The analysis response includes:
- ✅ **Document verification** (company name, document type, reporting period)
- 📊 **Financial metrics** (revenue, net income, EPS, margins, balance sheet highlights)
- 💡 **Investment recommendations** (buy/hold/sell thesis, valuation analysis)
- ⚠️ **Risk assessment** (financial, operational, market, and regulatory risks)
