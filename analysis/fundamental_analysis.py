import yfinance as yf

# Alias for the import in inference.py
def get_fundamentals(ticker_symbol):
    """Wrapper around fetch_fundamentals for consistency"""
    return fetch_fundamentals(ticker_symbol)

def get_stock_profile(ticker):
    import yfinance as yf
    info = yf.Ticker(ticker).info
    return {
        "ticker": ticker,
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "exchange": info.get("exchange"),
        "currency": info.get("currency"),
        "market_cap": info.get("marketCap"),
        "website": info.get("website")
    }

def fetch_fundamentals(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    financials = ticker.financials
    balance_sheet = ticker.balance_sheet
    cashflow = ticker.cashflow
    dividends = ticker.dividends
    history = ticker.history(period="5y")

    result = {
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "valuation": {
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "pb_ratio": info.get("priceToBook"),
            "peg_ratio": info.get("pegRatio")
        },
        "profitability": {
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "operating_margin": info.get("operatingMargins")
        },
        "dividends": {
            "yield": info.get("dividendYield"),
            "rate": info.get("dividendRate"),
            "payout_ratio": info.get("payoutRatio")
        },
        "financials": {
            "income_statement": financials.to_dict(),
            "balance_sheet": balance_sheet.to_dict(),
            "cash_flow": cashflow.to_dict()
        },
        "dividend_history": dividends.tail().to_dict(),
        "price_history": history.tail().to_dict()
    }

    return result

# data = fetch_fundamentals("TCS.NS")
# print(data)

#sector comparision function
def compare_peers(data_list):
    return sorted(data_list, key=lambda x: x["valuation"]["pe_ratio"] or float("inf"))

#risk analysis function
def compute_risk(ticker):
    import yfinance as yf
    df = yf.Ticker(ticker).history(period="1y", interval="1d")["Close"].dropna()
    drawdown = (df.max() - df.min()) / df.max()
    return {"max_drawdown": round(drawdown, 3)}

# Aliases for missing functions
def get_risk_metrics(ticker):
    """Wrapper around compute_risk"""
    return compute_risk(ticker)

def get_peer_comparison(ticker):
    """Placeholder for peer comparison"""
    return {"pe_rank": 0.5, "roe_rank": 0.5}

def get_technicals(ticker):
    """Placeholder for technical analysis"""
    return {
        "price_above_ma200": True,
        "macd_bullish": True,
        "rsi": 50,
        "bollinger_lower_touch": False
    }

def get_sentiment(ticker):
    """Placeholder for sentiment analysis"""
    return {
        "avg_score": 0.5,
        "label": "neutral"
    }

def get_earnings_forecast(ticker):
    """Placeholder for earnings forecast"""
    return {
        "next_earnings_date": "TBD",
        "eps_forecast": None
    }

def get_toon_summary(ticker, profile, fundamentals, technicals, sentiment, risk, peers, earnings):
    """Generate a Toon-style summary"""
    return f"""
analysis_date: 2025-11-12
investment_horizon: long_term
strategy_focus: multi-factor conviction-based allocation
ticker: {ticker}
company: {profile.get('company', 'N/A')}
sector: {profile.get('sector', 'N/A')}
valuation:
  pe_ratio: {fundamentals.get('valuation', {}).get('pe_ratio', 'N/A')}
  pb_ratio: {fundamentals.get('valuation', {}).get('pb_ratio', 'N/A')}
technicals:
  price_above_ma200: {technicals.get('price_above_ma200', False)}
sentiment:
  avg_score: {sentiment.get('avg_score', 0.5)}
risk:
  max_drawdown: {risk.get('max_drawdown', 'N/A')}
"""

