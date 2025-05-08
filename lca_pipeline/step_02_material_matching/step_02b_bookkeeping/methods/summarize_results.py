import json
from pathlib import Path

def summarize_inferences(base_dir, output_dir):
    base_dir = Path(base_dir)

    for element_dir in base_dir.iterdir():
        if not element_dir.is_dir():
            continue

        summary = {
            "name": element_dir.name,
            "total_steps": 0,
            "total_tokens": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_processing_time": 0.0,
            "inference_steps": [],
            "llm_responses": []
        }

        for file in sorted(element_dir.iterdir()):
            if not file.name.endswith(".json") or file.name.startswith("summary"):
                continue

            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            meta = data.get("llm_metadata", {})
            llm_response = data.get("llm_response", {})

            token_usage = meta.get("token_usage", {})
            summary["total_steps"] += 1
            summary["total_tokens"] += token_usage.get("total_tokens", 0)
            summary["total_prompt_tokens"] += token_usage.get("prompt_tokens", 0)
            summary["total_completion_tokens"] += token_usage.get("completion_tokens", 0)
            summary["total_processing_time"] += meta.get("processing_time", 0.0)

            summary["inference_steps"].append({
                "step": meta.get("step"),
                "matched_type": meta.get("matched_type"),
                "matched_name": meta.get("matched_name"),
                "matched_path": meta.get("matched_path"),
                "message": meta.get("message")
            })

            summary["llm_responses"].append(llm_response)

        # Save the summary to the same directory
        summary_path = output_dir / f"{summary['name']}_inference.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
