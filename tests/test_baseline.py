from unittest.mock import Mock, patch
from agentic_research_rag.agent.baseline import BaselineAgent

@patch("agentic_research_rag.agent.baseline.generate_text")
def test_baseline_agent(mock_generate_text):
    mock_generate_text.return_value = "This is a baseline answer."
    
    agent = BaselineAgent()
    answer = agent.run("What is quantum computing?")
    
    assert answer == "This is a baseline answer."
    mock_generate_text.assert_called_once()
    
    # Check that it passed the correct prompt
    call_args = mock_generate_text.call_args.args
    prompt = call_args[0]
    assert "What is quantum computing?" in prompt
