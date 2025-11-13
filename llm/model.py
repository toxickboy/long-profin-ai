from pydantic import BaseModel
from typing import List, Optional

class InvestmentDecision(BaseModel):
    asset: str
    action: str  # "buy", "hold", or "avoid"
    confidence: float  # 0.0 to 1.0
    allocation_pct: Optional[float]  # null if not buying
    rationale: str

class InferenceResponse(BaseModel):
    reasoning: str
    investment_decisions: List[InvestmentDecision]