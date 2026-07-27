# Spec 7: Multi-LLM Architecture

## Goal
Optimize our LangGraph agent by routing specific tasks to specialized language models based on their cost, latency, and reasoning capabilities, moving away from relying on a single model for everything.

## Scope
- Introduce support for Anthropic models alongside OpenAI models.
- Update `config.py` to define specific roles: `router_model`, `planner_model`, and `synthesis_model`.
- Refactor `AgentNodes` to dynamically load the router (`gpt-3.5-turbo` or `gpt-4o-mini`) and planner (`gpt-4o-mini`) models.
- Refactor the `Synthesizer` to use the `Anthropic` client and Claude API (`claude-3-haiku-20240307`) to write the final answers.
- Ensure all tests pass with the new Multi-LLM mocks.
