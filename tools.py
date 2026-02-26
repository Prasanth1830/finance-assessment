## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
@tool("Financial Document Reader")
def read_data_tool(path: str = 'data/sample.pdf') -> str:
    """Tool to read data from a pdf file from a path

    Args:
        path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

    Returns:
        str: Full Financial Document file
    """
    
    docs = PyPDFLoader(file_path=path).load()

    full_report = ""
    for data in docs:
        # Clean and format the financial document data
        content = data.page_content
        
        # Remove extra whitespaces and format properly
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")
            
        full_report += content + "\n"
        
    return full_report

## Creating Investment Analysis Tool
@tool("Investment Analyzer")
def analyze_investment_tool(financial_document_data: str) -> str:
    """Analyze financial document data for investment insights.

    Args:
        financial_document_data (str): The financial document text to analyze.

    Returns:
        str: Investment analysis results.
    """
    # Process and analyze the financial document data
    processed_data = financial_document_data
    
    # Clean up the data format
    i = 0
    while i < len(processed_data):
        if processed_data[i:i+2] == "  ":  # Remove double spaces
            processed_data = processed_data[:i] + processed_data[i+1:]
        else:
            i += 1
            
    return processed_data

## Creating Risk Assessment Tool
@tool("Risk Assessment Tool")
def create_risk_assessment_tool(financial_document_data: str) -> str:
    """Create a risk assessment from financial document data.

    Args:
        financial_document_data (str): The financial document text to assess risk for.

    Returns:
        str: Risk assessment results.
    """
    return financial_document_data