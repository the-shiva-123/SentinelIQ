from __future__ import annotations

import sys
from pathlib import Path

# Bring project root into scope path context
sys.path.append(str(Path(__file__).resolve().parents[1]))

from copilot.rag import VectorRAGEngine
from copilot.graph import CopilotWorkflowGraph
from copilot.evaluation import RAGEvaluator

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m copilot.cli [index|ask|evaluate] [optional_query]")
        sys.exit(1)

    command = sys.argv[1].lower()
    
    if command == "index":
        # Simulates loading golden dataset files into the indexer
        import json
        golden_jsonl = Path("data/golden/knowledge_documents_v001.jsonl")
        docs = []
        if golden_jsonl.exists():
            with open(golden_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        docs.append(json.loads(line))
        else:
            docs = [{"full_content": "Sample system telemetry record context."}]
            
        engine = VectorRAGEngine()
        engine.build_index(docs)

    elif command == "ask":
        query = sys.argv[2] if len(sys.argv) > 2 else "Which release first introduced ERR_AUTH_401?"
        workflow = CopilotWorkflowGraph().compile_graph()
        output = workflow.invoke({"query": query})
        
        print(f"=== SentinelIQ RAG System Retrieval Inquiry ===")
        print(f"Question: \"{query}\"\n")
        print("[Cited Answer Response]:")
        print("----------------------------------------------------------------------")
        print(output["generation_output"])
        print("----------------------------------------------------------------------")

    elif command == "evaluate":
        evaluator = RAGEvaluator()
        evaluator.run_suite()

if __name__ == "__main__":
    main()