import os
from datetime import datetime

from dotenv import load_dotenv

from agentic_research_rag.agent.baseline import BaselineAgent
from agentic_research_rag.agent.graph import ResearchAgent
from agentic_research_rag.evaluation.evaluator import Evaluator
from agentic_research_rag.logger import logger

load_dotenv()


def run_benchmarks():
    topics = [
        "What are the latest breakthroughs in solid-state batteries as of 2024?",
        "Compare the economic policies of the US and EU regarding artificial intelligence.",
        "What is the history and current status of the James Webb Space Telescope?",
    ]

    baseline_agent = BaselineAgent()
    research_agent = ResearchAgent()
    evaluator = Evaluator()

    report_lines = [
        "# Agentic RAG vs Baseline Benchmarking Report",
        f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "This report evaluates the performance of the Agentic RAG pipeline against a Baseline LLM.",
        "Scores are out of 5 for Comprehensiveness (Comp), Recency (Rec), Factual Accuracy (Acc), and Citations (Cit).",
        "",
        "| Topic | Winner | Baseline (Comp/Rec/Acc/Cit) | Agent (Comp/Rec/Acc/Cit) |",
        "|---|---|---|---|",
    ]

    for topic in topics:
        logger.info(f"--- Benchmarking Topic: {topic} ---")

        # 1. Run Baseline
        logger.info("Running Baseline Agent...")
        baseline_answer = baseline_agent.run(topic)

        # 2. Run Agentic RAG
        logger.info("Running Agentic RAG...")
        agent_answer = ""
        for event in research_agent.stream_run(topic):
            for node_name, state_update in event.items():
                if node_name == "synthesize" or node_name == "classify":
                    agent_answer = state_update.get("final_answer", agent_answer)
                
        # 3. Evaluate
        logger.info("Evaluating answers...")
        result = evaluator.evaluate_answers(topic, baseline_answer, agent_answer)

        logger.info(f"Winner: {result.winner.upper()}")
        logger.info(f"Justification: {result.final_justification}")

        b_score = result.baseline_score
        a_score = result.agent_score

        b_str = f"{b_score.comprehensiveness}/{b_score.recency}/{b_score.accuracy}/{b_score.citations}"
        a_str = f"{a_score.comprehensiveness}/{a_score.recency}/{a_score.accuracy}/{a_score.citations}"

        report_lines.append(f"| {topic} | **{result.winner.upper()}** | {b_str} | {a_str} |")

    # Save the markdown report
    output_dir = "outputs/reports"
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "benchmark_report.md")
    
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))
        
    logger.info(f"Benchmarking complete. Report saved to: {report_path}")

if __name__ == "__main__":
    run_benchmarks()
