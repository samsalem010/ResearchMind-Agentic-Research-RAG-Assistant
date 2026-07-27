import os
from pathlib import Path
from agentic_research_rag.reporting.reporter import Reporter

def test_reporter_sanitizes_filename(tmp_path):
    reporter = Reporter(reports_dir=str(tmp_path))
    safe_name = reporter._sanitize_filename("What is the meaning of life?!!!")
    assert safe_name == "what_is_the_meaning_of_life"

def test_reporter_generates_markdown(tmp_path):
    reporter = Reporter(reports_dir=str(tmp_path))
    topic = "Quantum Computing"
    content = "Quantum computing uses qubits."
    
    filepath = reporter.generate_markdown_report(topic, content)
    
    assert os.path.exists(filepath)
    assert filepath.endswith(".md")
    
    with open(filepath, "r", encoding="utf-8") as f:
        file_content = f.read()
        assert "# Research Report: Quantum Computing" in file_content
        assert "Quantum computing uses qubits." in file_content
