## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, read_data_tool

## Creating a task to verify the document
verification = Task(
    description="Verify that the uploaded document at {file_path} is a valid financial document.\n\
Use the Financial Document Reader tool with path='{file_path}' to read the document.\n\
Identify: the company name, reporting period, document type (10-K, 10-Q, earnings release, etc.).\n\
Confirm that it contains actual financial data such as revenue, expenses, assets, liabilities, etc.\n\
Provide a brief summary of what the document contains.",

    expected_output="""A structured verification report containing:
- Document type (e.g., 10-K, 10-Q, Earnings Release, Annual Report)
- Company name and ticker symbol
- Reporting period covered
- Confirmation that the document contains valid financial data
- Brief summary of key sections found in the document""",

    agent=verifier,
    tools=[read_data_tool],
    async_execution=False,
)

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="Analyze the financial document at {file_path} thoroughly to answer the user's query: {query}\n\
Use the Financial Document Reader tool with path='{file_path}' to read the document.\n\
Extract key financial metrics including revenue, net income, EPS, margins, and other relevant data.\n\
Provide detailed analysis with specific numbers and trends from the document.\n\
Search the internet for relevant market context and comparable company data.\n\
Base all analysis on actual data found in the document.",

    expected_output="""A comprehensive financial analysis report containing:
- Executive summary of key findings
- Key financial metrics with actual numbers from the document
- Revenue and profitability analysis with trends
- Balance sheet highlights
- Cash flow analysis
- Comparison with industry benchmarks where relevant
- Key takeaways and implications for investors""",

    agent=financial_analyst,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="Based on the financial analysis of the document at {file_path}, provide investment recommendations.\n\
Consider the user's query: {query}\n\
Use the Financial Document Reader tool with path='{file_path}' if additional document details are needed.\n\
Evaluate the company's financial health, growth prospects, competitive position, and valuation.\n\
Search the internet for current market conditions, analyst ratings, and comparable company valuations.\n\
Provide balanced recommendations considering both opportunities and risks.",

    expected_output="""A structured investment recommendation report containing:
- Investment thesis summary
- Key strengths and competitive advantages
- Growth drivers and catalysts
- Valuation analysis (P/E, P/S, EV/EBITDA comparisons)
- Risk factors to consider
- Actionable investment recommendations with rationale
- Suggested position sizing and entry/exit considerations
- Links to relevant market research and data sources""",

    agent=investment_advisor,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="Conduct a comprehensive risk assessment based on the financial document at {file_path}.\n\
Evaluate the user's query context: {query}\n\
Use the Financial Document Reader tool with path='{file_path}' if additional document details are needed.\n\
Identify and analyze key risk factors including financial risks, operational risks, market risks, and regulatory risks.\n\
Assess the company's debt levels, liquidity position, and financial stability.\n\
Search for industry-specific risk factors and macroeconomic considerations.",

    expected_output="""A detailed risk assessment report containing:
- Overall risk rating (Low/Medium/High) with justification
- Financial risk analysis (leverage, liquidity, solvency ratios)
- Operational risk factors
- Market and competitive risks
- Regulatory and compliance risks
- Risk mitigation strategies and recommendations
- Stress test scenarios and their potential impact
- Summary of key risk indicators to monitor""",

    agent=risk_assessor,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)