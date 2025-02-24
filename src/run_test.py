import sys
import os
import asyncio

#sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
from open_deep_research.state import ReportState
import open_deep_research.utils as utils


test_config = {
    "configurable": {
        "thread_id": "dummy-thread",
        "planner_provider": "openai",
        "planner_model": "gpt-4o-mini",
        "writer_provider": "openai",
        "writer_model": "gpt-4o-mini",
        "max_search_depth": 2,
        "number_of_queries": 2,
    }
}

output_dir = "markdown_examples"
os.makedirs(output_dir, exist_ok=True)

async def build_and_run_graph():
    datapoints = [1]
    for i in datapoints:
        dummy_state = ReportState({
            "topic": "",
            "type": "",
            "reference": "", 
            "formatted_metadata": "", 
            "feedback_on_report_plan": "",
            "sections": [],
            "completed_sections": [],
            "report_sections_from_research": "",
            "final_report": ""
        })

        memory = MemorySaver()
        graph = builder.compile(checkpointer=memory)
        
        print("running graph")
        async for event in graph.astream(dummy_state, test_config, stream_mode="updates"):
            print("Event:", event)
            print('\n')
        
        # Retrieve final state after execution
        final_state = graph.get_state(test_config)
        final_report = final_state.values.get("final_report", "")
        output_file = os.path.join(output_dir, f"final_report_{i}.md")
        # Save as markdown
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_report)

if __name__ == '__main__':
    asyncio.run(build_and_run_graph())
