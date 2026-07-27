import time
from agentic_research_rag.agent.graph import ResearchAgent

print("Initializing ResearchAgent...")
agent = ResearchAgent()

def run_test(topic: str):
    print("\n" + "="*50)
    print(f"Running pipeline for topic: '{topic}'")
    print("="*50)
    
    start_time = time.time()
    
    # We will run standard graph execution
    # This will plan queries, fetch Perplexity results, chunk, embed, index and synthesize
    answer = agent.run(topic)
    
    duration = time.time() - start_time
    print(f"Pipeline finished in {duration:.2f} seconds.")
    print("\n--- Final Answer Preview ---")
    print(answer[:500] + "...")
    print("----------------------------")

# 1. Run for "iphone" (First Run - should search and save)
run_test("iphone")

# 2. Run for "iphone" again (Second Run - should hit exact cache and complete immediately)
run_test("iphone")
