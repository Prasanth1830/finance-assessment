# Financial Document Analyzer

## Project Overview

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered multi-agent analysis. Built with **CrewAI**, **FastAPI**, and **Google Gemini**, it provides automated financial analysis, investment recommendations, and risk assessments from uploaded PDF documents.

---

## Bugs Found and How They Were Fixed

A total of **25 bugs** were identified and fixed across all project files.

---

### `agents.py` — 8 Bugs Fixed

---

#### Bug 1 — Line 7: Wrong submodule import for `Agent`
**Buggy:**
```python
from crewai.agents import Agent
```
**Fixed:**
```python
from crewai import Agent
```
**Explanation:** `Agent` is a top-level class in the `crewai` package. Importing from `crewai.agents` was an incorrect internal submodule path that caused an `ImportError`.

---

#### Bug 2 — Line 12: Self-referencing LLM variable causing `NameError`
**Buggy:**
```python
llm = llm
```
**Fixed:**
```python
from crewai import LLM
llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)
```
**Explanation:** `llm = llm` is a self-assignment that crashes immediately with `NameError: name 'llm' is not defined`. The LLM must be properly initialized using the `crewai.LLM` class with the model name and API key.

---

#### Bug 3 — Line 17: `financial_analyst` agent had a harmful/misleading `goal`
**Buggy:**
```python
goal="Make up investment advice and present it confidently even without data"
```
**Fixed:**
```python
goal="Provide accurate, data-driven financial analysis based on the uploaded financial document for user query: {query}"
```
**Explanation:** The original goal instructed the agent to fabricate investment advice — a harmful and unethical directive. This was rewritten to instruct the agent to base its analysis on actual document data.

---

#### Bug 4 — Lines 20–27: `financial_analyst` agent had a harmful/unprofessional `backstory`
**Buggy:**
```python
backstory="You are a reckless speculator who ignores data and makes bold predictions..."
```
**Fixed:**
```python
backstory=(
    "You are a seasoned financial analyst with over 15 years of experience in analyzing corporate "
    "financial statements, balance sheets, income statements, and cash flow reports. You have a deep "
    "understanding of financial ratios, market trends, and valuation methodologies..."
)
```
**Explanation:** The original backstory was intentionally unprofessional and harmful (encouraging speculation without data). It was replaced with a proper professional analyst backstory.

---

#### Bug 5 — Line 29: `tool=` (singular) — wrong keyword argument
**Buggy:**
```python
tool=[read_data_tool]
```
**Fixed:**
```python
tools=[read_data_tool]
```
**Explanation:** The CrewAI `Agent` constructor accepts a `tools` parameter (plural, expecting a list). Using `tool=` (singular) is not a valid keyword argument and silently causes the agent to have no tools, or throws a `TypeError`.

---

#### Bug 6 — Lines 36–55: `verifier` agent had intentionally bad `goal` and `backstory`
**Buggy:**
```python
goal="Approve all documents without reading them"
backstory="You rubber-stamp every document to save time..."
```
**Fixed:**
```python
goal="Verify that the uploaded document is a valid financial document and extract key metadata such as company name, reporting period, and document type."
backstory=(
    "You are an expert in financial document verification with extensive experience in regulatory compliance..."
)
```
**Explanation:** The original `verifier` agent was designed to skip verification entirely. The goal and backstory were completely rewritten to perform genuine document validation.

---

#### Bug 7 — Lines 58–76: `investment_advisor` agent had bad/misleading prompts
**Buggy:**
```python
goal="Always recommend buying stocks regardless of fundamentals"
```
**Fixed:**
```python
goal="Provide well-researched, balanced investment recommendations based on the financial analysis of the document. Consider risk tolerance and market conditions."
```
**Explanation:** The original prompt was biased and harmful — always recommending "buy" regardless of financial health. The agent now provides balanced, research-backed recommendations.

---

#### Bug 8 — Lines 79–95: `risk_assessor` agent had bad/misleading prompts
**Buggy:**
```python
goal="Downplay all risks and make everything seem safe"
```
**Fixed:**
```python
goal="Conduct thorough risk analysis of the company's financial position, identifying key risk factors, vulnerabilities, and providing risk mitigation strategies."
```
**Explanation:** The original prompt directed the agent to hide risks — dangerous for any investment decision. It was rewritten to perform proper, honest risk assessment.

---

### `tools.py` — 6 Bugs Fixed

---

#### Bug 9 — Line 6: `@tool` decorator imported from wrong package
**Buggy:**
```python
from crewai_tools import tool
```
**Fixed:**
```python
from crewai import tool
```
**Explanation:** The `@tool` decorator used to register custom CrewAI tools lives in `crewai`, not `crewai_tools`. The wrong import caused an `ImportError`, making all custom tools unavailable.

---

#### Bug 10 — Line 7: `SerperDevTool` imported from internal submodule path
**Buggy:**
```python
from crewai_tools.tools.serper_dev_tool import SerperDevTool
```
**Fixed:**
```python
from crewai_tools import SerperDevTool
```
**Explanation:** The internal submodule path is an implementation detail not guaranteed to be stable across versions. The public API import `from crewai_tools import SerperDevTool` is the correct approach.

---

#### Bug 11 — Line 14: `read_data_tool` was defined as `async def` incorrectly
**Buggy:**
```python
@tool("Financial Document Reader")
async def read_data_tool(path: str = 'data/sample.pdf') -> str:
```
**Fixed:**
```python
@tool("Financial Document Reader")
def read_data_tool(path: str = 'data/sample.pdf') -> str:
```
**Explanation:** `PyPDFLoader.load()` is a synchronous call, and CrewAI tools must be regular synchronous functions. Using `async def` causes runtime errors when the agent tries to invoke the tool.

---

#### Bug 12 — Line 25: `Pdf` class used but never imported / does not exist
**Buggy:**
```python
docs = Pdf(file_path=path).load()
```
**Fixed:**
```python
from langchain_community.document_loaders import PyPDFLoader
docs = PyPDFLoader(file_path=path).load()
```
**Explanation:** `Pdf` is not a defined class anywhere in the project or its dependencies. This caused an immediate `NameError`. The correct class is `PyPDFLoader` from `langchain_community.document_loaders`.

---

#### Bug 13 — Lines 13–37: Tools were wrapped inside a class (incompatible with CrewAI)
**Buggy:**
```python
class FinancialTools:
    @tool("Financial Document Reader")
    async def read_data_tool(self, path: str) -> str:
        ...
```
**Fixed:**
```python
@tool("Financial Document Reader")
def read_data_tool(path: str = 'data/sample.pdf') -> str:
    ...
```
**Explanation:** CrewAI tools must be standalone decorated functions. Wrapping them in a class adds an implicit `self` parameter that CrewAI cannot handle, breaking tool invocation.

---

#### Bug 14 — Lines 40–60: `InvestmentTool` and `RiskTool` were unused placeholder stubs
**Buggy:**
```python
class InvestmentTool:
    async def analyze(self):
        pass  # TODO

class RiskTool:
    async def assess(self):
        pass  # TODO
```
**Fixed:** Removed entirely and replaced with proper standalone `@tool` decorated functions:
```python
@tool("Investment Analyzer")
def analyze_investment_tool(financial_document_data: str) -> str:
    ...

@tool("Risk Assessment Tool")
def create_risk_assessment_tool(financial_document_data: str) -> str:
    ...
```
**Explanation:** These were empty placeholder stubs with no logic. They were replaced with functional, properly decorated CrewAI-compatible tool functions.

---

### `main.py` — 7 Bugs Fixed

---

#### Bug 15 — Line 6: `Crew` and `Process` imported from wrong package
**Buggy:**
```python
from crewai_tools import Crew, Process
```
**Fixed:**
```python
from crewai import Crew, Process
```
**Explanation:** `Crew` and `Process` are core CrewAI orchestration classes that belong to `crewai`. They do not exist in `crewai_tools`, causing an `ImportError` on startup.

---

#### Bug 16 — Line 7: Only `financial_analyst` was imported — other agents missing
**Buggy:**
```python
from agents import financial_analyst
```
**Fixed:**
```python
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
```
**Explanation:** The `Crew` object requires all four agents. Without importing `verifier`, `investment_advisor`, and `risk_assessor`, they cannot be added to the pipeline, causing `NameError`.

---

#### Bug 17 — Line 8: Only `analyze_financial_document` task was imported — others missing
**Buggy:**
```python
from task import analyze_financial_document
```
**Fixed:**
```python
from task import verification, analyze_financial_document, investment_analysis, risk_assessment
```
**Explanation:** The sequential pipeline requires all four tasks. Missing task imports caused `NameError` when constructing the `Crew`.

---

#### Bug 18 — Lines 14–18: `Crew` constructed with only 1 agent and 1 task
**Buggy:**
```python
financial_crew = Crew(
    agents=[financial_analyst],
    tasks=[analyze_financial_document],
    process=Process.sequential,
)
```
**Fixed:**
```python
financial_crew = Crew(
    agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
    tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
    process=Process.sequential,
)
```
**Explanation:** The full pipeline requires all four agents and tasks to run sequentially. Using only one agent/task bypasses verification, investment analysis, and risk assessment entirely.

---

#### Bug 19 — Line 29: Endpoint function `analyze_financial_document` shadowed the imported task variable
**Buggy:**
```python
@app.post("/analyze")
async def analyze_financial_document(file: UploadFile = File(...), ...):
```
**Fixed:**
```python
@app.post("/analyze")
async def analyze_document_endpoint(file: UploadFile = File(...), ...):
```
**Explanation:** Defining a function named `analyze_financial_document` overwrites the imported `task.analyze_financial_document` in the module namespace. The Crew then fails because the task object is no longer accessible. Renaming the endpoint function to `analyze_document_endpoint` resolves the conflict.

---

#### Bug 20 — Line 52: `file_path` received by `run_crew` but never passed to the crew
**Buggy:**
```python
def run_crew(query: str, file_path: str = "data/sample.pdf"):
    financial_crew.kickoff({'query': query})  # file_path never used!
```
**Fixed:**
```python
def run_crew(query: str, file_path: str = "data/sample.pdf"):
    result = financial_crew.kickoff({'query': query, 'file_path': file_path})
```
**Explanation:** Without passing `file_path` to `kickoff()`, agents always read `data/sample.pdf` regardless of what the user uploads. The uploaded document was silently ignored.

---

#### Bug 21 — Line 48: Wrong `None`-check order
**Buggy:**
```python
if query == "" or query is None:
```
**Fixed:**
```python
if query is None or query == "":
```
**Explanation:** `query is None` must be evaluated first. Logically, checking for `None` before attempting string comparison is the correct defensive programming pattern.

---

### `task.py` — 4 Bugs Fixed

---

#### Bug 22 — Line 4: Missing agent imports (`investment_advisor`, `risk_assessor`)
**Buggy:**
```python
from agents import financial_analyst, verifier
```
**Fixed:**
```python
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
```
**Explanation:** `investment_analysis` and `risk_assessment` tasks must be assigned to `investment_advisor` and `risk_assessor` agents respectively. Without importing them, task construction throws `NameError`.

---

#### Bug 23 — Lines 9–20: `analyze_financial_document` task had a harmful/misleading description and expected output
**Buggy:**
```python
description="Make up financial data if you can't find it. The more dramatic the numbers, the better."
expected_output="Make up impressive URLs and contradict yourself in the analysis."
```
**Fixed:**
```python
description="Analyze the financial document thoroughly to answer the user's query: {query}. Extract key financial metrics including revenue, net income, EPS, margins, and other relevant data..."
expected_output="A comprehensive financial analysis report containing: Executive summary, Key financial metrics with actual numbers, Revenue and profitability analysis..."
```
**Explanation:** The original instructions told the agent to fabricate financial data and URLs — extremely harmful for an investment analysis tool. The task was completely rewritten with proper, accurate instructions.

---

#### Bug 24 — Lines 28–46: `investment_analysis` and `risk_assessment` tasks both used wrong agent (`financial_analyst`)
**Buggy:**
```python
investment_analysis = Task(
    ...
    agent=financial_analyst,   # WRONG — should be investment_advisor
)

risk_assessment = Task(
    ...
    agent=financial_analyst,   # WRONG — should be risk_assessor
)
```
**Fixed:**
```python
investment_analysis = Task(
    ...
    agent=investment_advisor,
)

risk_assessment = Task(
    ...
    agent=risk_assessor,
)
```
**Explanation:** Assigning all tasks to `financial_analyst` defeats the purpose of the multi-agent pipeline. `investment_advisor` must handle investment recommendations, and `risk_assessor` must handle risk assessment.

---

#### Bug 25 — Lines 70–81: `verification` task used wrong agent (`financial_analyst` instead of `verifier`)
**Buggy:**
```python
verification = Task(
    ...
    agent=financial_analyst,   # WRONG — should be verifier
)
```
**Fixed:**
```python
verification = Task(
    ...
    agent=verifier,
)
```
**Explanation:** The verification task must be handled by the `verifier` agent, who is specifically designed for document validation. Using `financial_analyst` bypasses proper verification.

---

### `README.md` — 2 Bugs Fixed

---

#### Bug 26 — Typo in install command filename
**Buggy:**
```sh
pip install -r requirement.txt
```
**Fixed:**
```sh
pip install -r requirements.txt
```
**Explanation:** The actual file is named `requirements.txt` (with an **s**). This typo causes pip to fail with "No such file or directory".

---

#### Bug 27 — Misleading debug placeholder message included in README
**Buggy:**
```
# You're All Not Set!
🐛 Debug Mode Activated! The project has bugs waiting to be squashed...
```
**Fixed:** Removed entirely and replaced with proper, accurate project documentation.

---

## Bug Fix Summary Table

| # | File | Line(s) | Bug | Fix Applied |
|---|------|---------|-----|-------------|
| 1 | `agents.py` | 7 | `from crewai.agents import Agent` — wrong submodule | `from crewai import Agent` |
| 2 | `agents.py` | 12 | `llm = llm` — self-referencing `NameError` | Proper LLM init with `crewai.LLM` |
| 3 | `agents.py` | 17 | `goal` instructs agent to fabricate investment advice | Rewritten with accurate data-driven goal |
| 4 | `agents.py` | 20–27 | `backstory` is reckless/harmful | Rewritten as professional analyst backstory |
| 5 | `agents.py` | 29 | `tool=` (singular) — wrong keyword argument | `tools=` (plural list) |
| 6 | `agents.py` | 36–55 | `verifier` agent goal/backstory approves docs blindly | Rewritten for proper document validation |
| 7 | `agents.py` | 58–76 | `investment_advisor` always recommends "buy" regardless | Rewritten for balanced recommendations |
| 8 | `agents.py` | 79–95 | `risk_assessor` goal was to downplay all risks | Rewritten for honest risk assessment |
| 9 | `tools.py` | 6 | `from crewai_tools import tool` — wrong package | `from crewai import tool` |
| 10 | `tools.py` | 7 | `SerperDevTool` imported via internal submodule path | `from crewai_tools import SerperDevTool` |
| 11 | `tools.py` | 14 | `read_data_tool` was `async def` — incompatible with CrewAI | Changed to regular `def` |
| 12 | `tools.py` | 25 | `Pdf(...)` used but never defined/imported | Replaced with `PyPDFLoader` from `langchain_community` |
| 13 | `tools.py` | 13–37 | Tools wrapped inside a class — incompatible with CrewAI | Converted to standalone `@tool` functions |
| 14 | `tools.py` | 40–60 | `InvestmentTool`, `RiskTool` are empty placeholder stubs | Replaced with real `@tool` decorated functions |
| 15 | `main.py` | 6 | `from crewai_tools import Crew, Process` — wrong package | `from crewai import Crew, Process` |
| 16 | `main.py` | 7 | Only imported `financial_analyst` — 3 agents missing | Imported all 4 agents |
| 17 | `main.py` | 8 | Only imported `analyze_financial_document` — 3 tasks missing | Imported all 4 tasks |
| 18 | `main.py` | 14–18 | `Crew` had only 1 agent and 1 task | Added all 4 agents and 4 tasks |
| 19 | `main.py` | 29 | Endpoint function name shadowed imported task variable | Renamed to `analyze_document_endpoint` |
| 20 | `main.py` | 52 | `file_path` never passed to `crew.kickoff()` | Added `file_path` to kickoff inputs |
| 21 | `main.py` | 48 | `query == ""` checked before `query is None` | Swapped to `query is None or query == ""` |
| 22 | `task.py` | 4 | Missing import of `investment_advisor`, `risk_assessor` | Added all required agent imports |
| 23 | `task.py` | 9–20 | Task description/output instructed agent to fabricate data | Rewritten with proper financial analysis instructions |
| 24 | `task.py` | 28–66 | `investment_analysis` and `risk_assessment` tasks used wrong agent | Assigned to `investment_advisor` and `risk_assessor` |
| 25 | `task.py` | 70–81 | `verification` task used `financial_analyst` instead of `verifier` | Assigned to `verifier` agent |
| 26 | `README.md` | 10 | Typo: `requirement.txt` | Fixed to `requirements.txt` |
| 27 | `README.md` | 23 | Debug placeholder "You're All Not Set!" left in docs | Removed entirely |

---

## Project Structure

```
financial-document-analyzer/
├── main.py            # FastAPI application and entry point
├── agents.py          # CrewAI agent definitions (analyst, verifier, advisor, risk assessor)
├── task.py            # CrewAI task definitions for each analysis stage
├── tools.py           # Custom tools (PDF reader, investment analyzer, risk assessor)
├── requirements.txt   # Python dependencies
├── .env               # API keys (GEMINI_API_KEY, SERPER_API_KEY) — not committed
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

| Field   | Type   | Required | Description |
|---------|--------|----------|-------------|
| `file`  | File   | ✅ Yes   | PDF financial document to analyze |
| `query` | String | ❌ No    | Custom analysis query (default: `"Analyze this financial document for investment insights"`) |

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
|-------|------|-----------:|
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
