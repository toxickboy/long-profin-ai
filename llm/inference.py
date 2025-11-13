"""Stock signal inference module"""
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from llm.model import InferenceResponse, InvestmentDecision
from llm.prompt import SYSTEM_PROMPT


def get_signals(ticker: str, available_funds: Optional[float] = None) -> InferenceResponse:
    """
    Analyze a stock and return investment signals.
    
    Args:
        ticker: Stock ticker symbol
        available_funds: Optional available funds for allocation
        
    Returns:
        InferenceResponse with investment decision
    """
    # Import analysis functions inside function to avoid module-level import failures
    from analysis.fundamental_analysis import (
        get_stock_profile,
        get_fundamentals,
        get_technicals,
        get_sentiment,
        get_risk_metrics,
        get_peer_comparison,
        get_earnings_forecast,
        get_toon_summary
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
    toon_summary = get_toon_summary(
        ticker=ticker,
        profile=stock_profile,
        fundamentals=fundamentals,
        technicals=technicals,
        sentiment=sentiment,
        risk=risk,
        peers=peers,
        earnings=earnings
    )

    print("Toon Summary:", toon_summary)

    response = chain.invoke({
        "ticker": ticker,
        "available_funds": str(available_funds) if available_funds else "not mentioned",
        "toon_summary": toon_summary
    })

    return InferenceResponse(**response)