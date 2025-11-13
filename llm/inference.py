"""Stock signal inference module"""
from typing import Optional
from dotenv import load_dotenv
import json

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from llm.model import InferenceResponse, InvestmentDecision
from llm.prompt import SYSTEM_PROMPT


def get_signals(ticker: str) -> InferenceResponse:
    """
    Analyze a stock and return investment recommendation.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        InferenceResponse with buy/avoid decision, price range, and holding period
    """
    # Import analysis functions inside function to avoid module-level import failures
    from analysis.fundamental_analysis import (
        get_stock_profile,
        get_fundamentals,
        get_technicals,
        get_sentiment,
        get_risk_metrics,
        get_peer_comparison,
        get_earnings_forecast
    )
    
    # Initialize LLM chain inside function
    llm = ChatOpenAI(model_name="gpt-5")  
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
    output_parser = JsonOutputParser(pydantic_object=InferenceResponse)
    chain = prompt | llm | output_parser
    
    # Gather data
    stock_profile = get_stock_profile(ticker)
    fundamentals = get_fundamentals(ticker)
    technicals = get_technicals(ticker)
    sentiment = get_sentiment(ticker)
    risk = get_risk_metrics(ticker)
    peers = get_peer_comparison(ticker)
    earnings = get_earnings_forecast(ticker)
    
    # Create structured data dictionary instead of toon_summary
    structured_data = {
        "ticker": ticker,
        "company": stock_profile.get('company'),
        "sector": stock_profile.get('sector'),
        "fundamentals": {
            "valuation": fundamentals.get('valuation', {}),
            "profitability": fundamentals.get('profitability', {}),
            "dividends": fundamentals.get('dividends', {})
        },
        "technicals": technicals,
        "sentiment": sentiment,
        "risk": risk,
        "peers": peers,
        "earnings": earnings
    }

    print("Structured Data:", json.dumps(structured_data, indent=2, default=str))

    # Debug: Print what we're sending to the LLM
    print(f"\n=== Analyzing Ticker: {ticker} ===\n")
    
    response = chain.invoke({
        "ticker": ticker,
        "stock_data": json.dumps(structured_data, indent=2, default=str)
    })
    
    print(f"\n=== AI Response ===")
    print(json.dumps(response, indent=2, default=str))
    
    return InferenceResponse(**response)