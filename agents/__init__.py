"""
Chargeback Evidence AI - Agents Package
Modular multi-agent dispute intelligence engine.
Uses PEP 562 module lazy loading to avoid eager cascading imports.
"""

__all__ = [
    "OCRAgent",
    "NLPAgent",
    "EvidenceConsistencyEngine",
    "MLScoringAgent",
    "RAGAgent",
    "FraudIntelligenceAgent",
    "GeminiReportAgent"
]


def __getattr__(name: str):
    if name == "OCRAgent":
        from agents.ocr_agent import OCRAgent
        return OCRAgent
    elif name == "NLPAgent":
        from agents.nlp_agent import NLPAgent
        return NLPAgent
    elif name == "EvidenceConsistencyEngine":
        from agents.verification_engine import EvidenceConsistencyEngine
        return EvidenceConsistencyEngine
    elif name == "MLScoringAgent":
        from agents.ml_scoring_agent import MLScoringAgent
        return MLScoringAgent
    elif name == "RAGAgent":
        from agents.rag_agent import RAGAgent
        return RAGAgent
    elif name == "FraudIntelligenceAgent":
        from agents.fraud_intelligence import FraudIntelligenceAgent
        return FraudIntelligenceAgent
    elif name == "GeminiReportAgent":
        from agents.report_agent import GeminiReportAgent
        return GeminiReportAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
