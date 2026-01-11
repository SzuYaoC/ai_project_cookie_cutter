from typing import Dict, Any, Union, List
from app.core.llm.factory import get_chat_model
from app.core.eval.metrics import eval_answer_relevance, eval_faithfulness

async def evaluate_answer_relevance(query: str, answer: str) -> Dict[str, Any]:
    """
    Evaluate if the answer addresses the query using metrics module.
    """
    llm = get_chat_model()
    result = await eval_answer_relevance(query, answer, llm)
    return {
        "score": result.score,
        "passed": result.passed,
        "reasoning": result.details
    }

async def evaluate_faithfulness(context: Union[str, List[Dict]], answer: str) -> Dict[str, Any]:
    """
    Evaluate if the answer is faithful to the context using metrics module.
    """
    llm = get_chat_model()
    result = await eval_faithfulness(answer, context, llm)
    return {
        "score": result.score,
        "passed": result.passed,
        "reasoning": result.details
    }

async def evaluate_rag(query: str, context: Union[str, List[Dict]], answer: str) -> Dict[str, Any]:
    """
    Run all RAG metrics.
    """
    relevance = await evaluate_answer_relevance(query, answer)
    faithfulness = await evaluate_faithfulness(context, answer)
    
    return {
        "answer_relevance": relevance,
        "faithfulness": faithfulness,
        "overall_score": (relevance.get("score", 0) + faithfulness.get("score", 0)) / 2
    }


def evaluate_exact_match(expected: str, actual: str) -> float:
    """
    Simple exact match evaluation.
    """
    return 1.0 if expected.strip() == actual.strip() else 0.0
