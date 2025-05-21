from methods.prompt_builder_category import build_category_prompt
from methods.prompt_builder_category_ger import build_category_prompt_ger
from methods.prompt_builder_material import build_material_prompt
from methods.prompt_builder_material_ger import build_material_prompt_ger
from openai import OpenAI
import json
import re

# === Category Inference ===

# category llm interface
def category_inference(bim_element, category_data, mode, config):

    # Get language settings from config and build the prompt for category inference
    category_prompt_variables = config.get("category_prompt_variables", {})
    language = category_prompt_variables.get("language")

    if language == "en":
        prompt = build_category_prompt(bim_element, category_data, mode, config)
    else:
        prompt = build_category_prompt_ger(bim_element, category_data, mode, config)

    # Get model settings metadata for category inference
    category_config = config.get("category_inference_config", {})
    company_category_inference = category_config.get("company")
    key_category_inference = category_config.get("key")
    model_category_inference = category_config.get("model")
    temperature_category_inference = category_config.get("temperature")
    max_tokens_category_inference = category_config.get("max_tokens")

    # Conditional for company and client
    if company_category_inference == "OpenAI":
        category_client = OpenAI(api_key=key_category_inference)
    # Update later
    else:
        category_client = OpenAI(api_key=key_category_inference)

    # Pass the prompt with IFC data, the dissected LCI data, and the instructions to the LLM
    response = category_client.chat.completions.create(
        model=model_category_inference,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature_category_inference,
        max_tokens=max_tokens_category_inference
    )
    response_text = response.choices[0].message.content
    response_cleaned = re.sub(r"```json|```", "", response_text).strip()
    parsed_response = json.loads(response_cleaned)
    token_usage = response.usage
    return parsed_response, token_usage

# === Material Inference ===

# material llm interface
def material_inference(bim_element, material_data, mode, config, category=None):

    # Build the prompt for material inference
    prompt = build_material_prompt(bim_element, material_data, mode, config, category)

    # Get model settings metadata for material inference
    material_config = config.get("material_inference_config", {})
    company_material_inference = material_config.get("company")
    key_material_inference = material_config.get("key")
    model_material_inference = material_config.get("model")
    temperature_material_inference = material_config.get("temperature")
    max_tokens_material_inference = material_config.get("max_tokens")

    # Conditional for company and client
    if company_material_inference == "OpenAI":
        material_client = OpenAI(api_key=key_material_inference)
    # Update later
    else:
        material_client = OpenAI(api_key=key_material_inference)

    # Pass the prompt with IFC data, the dissected LCI data, and the instructions to the LLM
    response = material_client.chat.completions.create(
        model=model_material_inference,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature_material_inference,
        max_tokens=max_tokens_material_inference
    )
    response_text = response.choices[0].message.content
    response_cleaned = re.sub(r"```json|```", "", response_text).strip()
    parsed_response = json.loads(response_cleaned)
    token_usage = response.usage
    return parsed_response, token_usage