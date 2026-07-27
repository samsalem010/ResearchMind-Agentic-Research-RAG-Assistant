from unittest.mock import Mock, patch

from agentic_research_rag.evaluation.evaluator import Evaluator
from agentic_research_rag.evaluation.models import ComparisonResult, EvaluationScore


@patch("agentic_research_rag.evaluation.evaluator.shared_client")
def test_evaluator(mock_shared_client):
    mock_client = mock_shared_client
    
    # Mock the Instructor response
    mock_result = ComparisonResult(
        baseline_score=EvaluationScore(comprehensiveness=2, recency=3, accuracy=4, citations=1, reasoning="Basic"),
        agent_score=EvaluationScore(comprehensiveness=5, recency=5, accuracy=5, citations=5, reasoning="Excellent"),
        winner="agent",
        final_justification="The agent provided citations."
    )
    
    mock_client.chat.completions.create.return_value = mock_result
    
    evaluator = Evaluator()
    result = evaluator.evaluate_answers("test topic", "baseline text", "agent text")
    
    assert result.winner == "agent"
    assert result.baseline_score.citations == 1
    assert result.agent_score.comprehensiveness == 5
    mock_client.chat.completions.create.assert_called_once()
