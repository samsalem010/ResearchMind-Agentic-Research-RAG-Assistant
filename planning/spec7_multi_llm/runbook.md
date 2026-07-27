# spec7_multi_llm — Runbook

## Setup Requirements
1. **Environment Variables**: Ensure both `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are present in your `.env` file.
2. **Dependencies**: Run `pip install -e '.[dev]'` to ensure the new `anthropic` library is installed.

## Validation Commands
Run the test suite to verify the Multi-LLM mock logic is working seamlessly:
```bash
pytest tests/
```

If you want to run the pipeline manually via scratch scripts, you must supply valid API keys for both providers since the `Synthesizer` will attempt to call Anthropic and the `AgentNodes` will call OpenAI.
