from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from app.core.prompts.load_prompt import load_prompt_from_yaml

@dataclass
class EvalResult:
    score: float  # 0.0 to 1.0
    passed: bool
    details: str




async def eval_faithfulness(
    answer: str,
    context: Union[List[Dict[str, Any]], str],
    llm: Any
) -> EvalResult:
    """
    Use LLM to judge if the answer is grounded in the retrieved context.
    """
    # Load prompt from YAML
    prompt_template = load_prompt_from_yaml("app/core/prompts/templates/eval/faithfulness.yaml")
    
    # Format context
    if isinstance(context, list):
        context_text = "\n\n".join([
            f"[{i+1}] {chunk.get('text', chunk)}" 
            for i, chunk in enumerate(context)
        ])
    else:
        context_text = str(context)
    
    chain = prompt_template | llm
    resp = await chain.ainvoke({"context": context_text, "answer": answer})
    output = getattr(resp, "content", str(resp))
    
    # Parse response
    score = _parse_score(output)
    reason = _parse_reason(output)
    
    return EvalResult(
        score=score,
        passed=(score >= 0.8),
        details=reason
    )


async def eval_answer_relevance(
    question: str,
    answer: str,
    llm: Any
) -> EvalResult:
    """
    Use LLM to judge if the answer addresses the question.
    """
    # Load prompt from YAML
    prompt_template = load_prompt_from_yaml("app/core/prompts/templates/eval/answer_relevance.yaml")
    
    chain = prompt_template | llm
    resp = await chain.ainvoke({"question": question, "answer": answer})
    output = getattr(resp, "content", str(resp))
    
    score = _parse_score(output)
    reason = _parse_reason(output)
    
    return EvalResult(
        score=score,
        passed=(score >= 0.8),
        details=reason
    )



# ============================================================
# Helper Functions
# ============================================================
def _parse_score(text: str) -> float:
    """Extract score from LLM response."""
    match = re.search(r"SCORE:\s*([\d.]+)", text, re.IGNORECASE)
    if match:
        try:
            return min(1.0, max(0.0, float(match.group(1))))
        except ValueError:
            pass
    return 0.0


def _parse_reason(text: str) -> str:
    """Extract reason from LLM response."""
    match = re.search(r"REASON:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip().split('\n')[0]
    return text[:200] if text else "No reason provided"