# runner.py
import os
import json
from pathlib import Path
from methods.utils import create_inference_folders, load_yaml_config, simplify_lci_lists, simplify_category_list, simplify_material_lists
from methods.traverse import traverse_lci_hierarchy

def match_bim_files(input_dir, output_dir, lci_base_dir, mode_label):
    for filename in os.listdir(input_dir):
        if not filename.endswith(".json"):
            continue
        element_id = os.path.splitext(filename)[0]
        element_path = os.path.join(input_dir, filename)
        results_dir = os.path.join(output_dir, element_id)
        os.makedirs(results_dir, exist_ok=True)
        with open(element_path, "r", encoding="utf-8") as f:
            bim_element = json.load(f)
        print(f"> Processing {mode_label.upper()} → {element_id}")
        result = traverse_lci_hierarchy(
            bim_element=bim_element,
            current_dir=lci_base_dir,
            lci_base_dir=lci_base_dir,
            mode=mode_label,
            results_dir=results_dir,
            step=1
        )


def material_matcher():

    # setup paths & directories
    input_elements = Path("data/pipeline/step_01_data_extraction/step_01d_filter_data/Elements")
    input_target_layers = Path("data/pipeline/step_01_data_extraction/step_01d_filter_data/Target_Layers")
    inference_elements_folders = Path("data/pipeline/step_02_material_matching/step_02a_inference/Elements")
    inference_target_layers_folders = Path("data/pipeline/step_02_material_matching/step_02a_inference/Target_Layers")
    master_config_path = Path("config/master_config.yaml")

    # create folders for each element/target layer for recursive inference process
    create_inference_folders(input_elements, inference_elements_folders)
    create_inference_folders(input_target_layers, inference_target_layers_folders)

    # Get configurations from master_config.yaml
    master_config = load_yaml_config(master_config_path)
    config_database = master_config.get("database_config", {}).get("database")
    var_include_density = master_config.get("material_prompt_variables", {}).get("include_density")

    if config_database == "kbob":
        lci_base_dir = Path("data/input/LCI_database/KBOB")
        category_index_path = Path("data/input/LCI_database/KBOB/index.json")
        simplify_category_list(category_index_path) # make LLM friendly (minimize tokens)
        simplify_material_lists(lci_base_dir) # make LLM friendly (customizable, with include_density)

    else:
        lci_base_dir = Path("data/input/LCI_database/OEKOBAUDAT")
        category_index_path = Path("data/input/LCI_database/OEKOBAUDAT/index.json")
        simplify_lci_lists(lci_base_dir)
        #simplify_category_list(category_index_path) # make LLM friendly (minimize tokens)
        #simplify_material_lists(lci_base_dir, var_include_density) # make LLM friendly (customizable, with include_density) 

    # Match elements
    match_bim_files(
        input_dir=input_elements,
        output_dir=inference_elements_folders,
        lci_base_dir=lci_base_dir,
        mode_label="element"
    )

    # Match target layers
    match_bim_files(
        input_dir=input_target_layers,
        output_dir=inference_target_layers_folders,
        lci_base_dir=lci_base_dir,
        mode_label="layer"
    )

if __name__ == "__main__":
    material_matcher()
