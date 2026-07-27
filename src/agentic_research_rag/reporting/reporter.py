import os
import re
from datetime import datetime
from pathlib import Path

from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger


class Reporter:
    """
    Saves the final synthesized research answers as formatted Markdown reports.
    """

    def __init__(self, reports_dir: str | None = None):
        self.reports_dir = Path(reports_dir or settings.reports_dir)
        # Ensure the directory exists
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, topic: str) -> str:
        """
        Converts the topic into a safe, file-system friendly string.
        """
        # Convert to lowercase and replace spaces with underscores
        safe_name = topic.lower().strip().replace(" ", "_")
        # Remove any non-alphanumeric characters (except underscores and hyphens)
        safe_name = re.sub(r"[^\w\-]", "", safe_name)
        # Truncate to avoid overly long filenames
        return safe_name[:50]

    def generate_markdown_report(self, topic: str, content: str) -> str:
        """
        Generates a Markdown file with the final content and returns the file path.
        """
        logger.info(f"Generating markdown report for topic: '{topic}'")

        safe_topic = self._sanitize_filename(topic)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_topic}_{timestamp}.md"
        filepath = self.reports_dir / filename

        report_content = (
            f"# Research Report: {topic.title()}\n\n"
            f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"---\n\n"
            f"{content}\n"
        )

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report_content)
            logger.info(f"Successfully saved report to: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to generate report for '{topic}': {e}")
            raise
