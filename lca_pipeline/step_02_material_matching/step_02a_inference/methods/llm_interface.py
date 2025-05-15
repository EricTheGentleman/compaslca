from methods.prompt_builder import build_category_prompt, build_material_prompt
from methods.utils import load_yaml_config
from pathlib import Path
from openai import OpenAI
import json
import re

# === Category Inference ===

# config
master_config_path = Path("config/master_config.yaml")
master_config = load_yaml_config(master_config_path)
cat_inference_config = master_config.get("category_inference_config", {})
cat_key = cat_inference_config.get("api_key")
cat_client = OpenAI(api_key=cat_key)

# category llm interface
def category_inference(bim_element, category_data, mode):
    prompt = build_category_prompt(bim_element, category_data, mode)
    response = cat_client.chat.completions.create(
        model=cat_inference_config.get("model"),
        messages=[{"role": "user", "content": prompt}],
        temperature=cat_inference_config.get("temperature"),
        max_tokens=cat_inference_config.get("max_tokens")
    )
    response_text = response.choices[0].message.content
    response_cleaned = re.sub(r"```json|```", "", response_text).strip()
    parsed_response = json.loads(response_cleaned)
    token_usage = response.usage
    return parsed_response, token_usage

# === Material Inference ===

# config
mat_inference_config = master_config.get("material_inference_config", {})
mat_key = mat_inference_config.get("api_key")
mat_client = OpenAI(api_key=mat_key)

# material llm interface
def material_inference(bim_element, material_data, mode):
    prompt = build_material_prompt(bim_element, material_data, mode)
    response = mat_client.chat.completions.create(
        model=mat_inference_config.get("model"),
        messages=[{"role": "user", "content": prompt}],
        temperature=mat_inference_config.get("temperature"),
        max_tokens=mat_inference_config.get("max_tokens")
    )
    response_text = response.choices[0].message.content
    response_cleaned = re.sub(r"```json|```", "", response_text).strip()
    parsed_response = json.loads(response_cleaned)
    token_usage = response.usage
    return parsed_response, token_usage