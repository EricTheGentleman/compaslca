# prompt_builder.py
from methods.utils import load_yaml_config
from pathlib import Path
import json

master_config_path = Path("config/master_config.yaml")
master_config = load_yaml_config(master_config_path)

# === Category Prompt ===

# Get category prompt variables
cat_variables = master_config.get("category_prompt_variables", {})
cat_decision_justification = cat_variables.get("decision_justification")
cat_include_expert_reasoning  = cat_variables.get("include_expert_reasoning")
cat_include_cot = cat_variables.get("include_cot")

def build_category_prompt(bim_element, category_data, mode):
    json_string = json.dumps(bim_element, indent=2, ensure_ascii=False)
    category_json_string = json.dumps(category_data, indent=2, ensure_ascii=False)

    # Distinguish descriptor of first JSON file
    if mode == "element":
        descriptor = "**IfcBuildingElement**"
    elif mode == "target_layer":
        descriptor = "**Target Layer** of a IfcBuildingElement"
    else:
        descriptor = "**BIM Element**"

    # Expert Reasoning
    if cat_include_expert_reasoning == True:
        expert_reasoning = "You are an expert in life cycle assessment (LCA) and material classification. "
    else:
        expert_reasoning = ""

    # CoT
    if cat_include_cot == True:
        cot = "Analyze all possible entries and think step by step before making your decision. "
    else:
        cot = ""

    # Decision Justification
    if cat_decision_justification:
        comma = ","
        dec_just = '"Decision Justification": "<Insert decision justification here>"'
        justification_note = """
        
    **Decision Justification**
    - After choosing a material category, include a short justification that explains **which specific fields or properties** from the IFC element led to your decision.
    - Highlight any **textual clues** (like element name or material label), **geometric properties**, or **contextual data** that were useful in matching the element to the chosen category.
    - Keep the explanation clear and concise.

    """
    else:
        comma = ""
        dec_just = ""
        justification_note = ""


    prompt = f"""
    Given are two JSON files:

    1. A JSON file describing a {descriptor}:

    ```json
    {json_string}
    ```

    2. A JSON file listing **material or building element categories**:

    ```json
    {category_json_string}
    ```

    **Inference Task:**
    - Choose a "Material Category" from the database that best matches the {descriptor} described in the first JSON file.
    - If no viable category can be chosen, assign "None"
    {justification_note}
    ### **Required JSON Output Format:**
    Respond **ONLY** with valid JSON in the exact format below:
    ```json
    {{
        "Matched Material Category": "<Chosen Material Category | None>"{comma}
    {dec_just}
    }}

    ```
    **DO NOT** include explanations, commentary, or markdown formatting.
    """

    return prompt


# === Material Prompt ===

# Get material prompt variables
mat_variables = master_config.get("material_prompt_variables", {})
mat_include_expert_reasoning = mat_variables.get("include_expert_reasoning")
mat_include_cot = mat_variables.get("include_cot")
mat_decision_justification = mat_variables.get("decision_justification")
matching_strictness = mat_variables.get("matching_strictness")
    
def build_material_prompt(bim_element, material_data, mode):
    json_string = json.dumps(bim_element, indent=2, ensure_ascii=False)
    materials_json_string = json.dumps(material_data, indent=2, ensure_ascii=False)

    # Distinguish descriptor of first JSON file
    if mode == "element":
        descriptor = "**IfcBuildingElement**"
    elif mode == "target_layer":
        descriptor = "**Target Layer** of a IfcBuildingElement"
    else:
        descriptor = "**BIM Element**"

    # Expert Reasoning
    if mat_include_expert_reasoning == True:
        expert_reasoning = "You are an expert in life cycle assessment (LCA) and material classification. "
    else:
        expert_reasoning = ""

    # CoT
    if mat_include_cot == True:
        cot = "Analyze all possible entries and think step by step before making your decision. "
    else:
        cot = ""

    # Decision Justification
    if mat_decision_justification:
        comma = ","
        dec_just = '"Decision Justification": "<Insert decision justification here>"'
        justification_note = """

    **Justification Requirement:**
    - After selecting one or more material matches, explain why each entry was considered viable.
    - Reference specific fields from the IFC element or material entry that supported the decision.
    - Keep the explanation clear, concise, and grounded in the input data.

    """
    else:
        justification_note = ""
        comma = ""
        dec_just = ""


    prompt = f"""
    Given are two JSON files:

    1. A JSON file describing a {descriptor}:

    ```json
    {json_string}
    ```

    2. A JSON file for **predefined database containing standardized material definitions** of a previously inferred category:

    ```json
    {materials_json_string}
    ```
    {expert_reasoning}{cot}
    **Inference Task:**
    - Choose all viable “Material Options” entries from the database that best match the {descriptor} described in the first JSON file. 
    - The chosen materials do not have to be extact semantic matches, but rather viable approximations
    - If there is no exact match or viable approximation, assign an EMPTY list.
    {justification_note}
    ### **Required JSON Output Format:**
    Respond **ONLY** with valid JSON in the exact format below:
    ```json
    {{
    "Matched Material Name": ["<Material Name 1>", "<Material Name 2>", ...]{comma}  // Empty list if no match
    {dec_just}
    }}

    ```
    **DO NOT** include explanations, commentary, or markdown formatting.
    """
    return prompt