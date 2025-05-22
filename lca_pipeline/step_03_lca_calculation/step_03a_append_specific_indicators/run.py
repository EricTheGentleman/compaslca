from methods.lca_kbob import extract_kbob_data
from methods.lca_oekobaudat import extract_oekobaudat_data
from methods.append_quantities import append_quantities
from methods.utils import load_yaml_config
from pathlib import Path

# Master config path
master_config = Path("config/master_config.yaml")
config = load_yaml_config(master_config)
database_config = config["database_config"]
database_selection = database_config["database"]
boq_path = Path("data/pipeline/step_01_data_extraction/step_01c_dissect_layers/BoQ_step_01c.csv")

# Root folders of all (step-wise) inferences
llm_elements = Path("data/pipeline/step_02_material_matching/step_02b_bookkeeping/Elements")
llm_target_layers = Path("data/pipeline/step_02_material_matching/step_02b_bookkeeping/Target_Layers")


# Output folders indicators enhanced
output_base_dir = Path("data/pipeline/step_03_lca_calculation/step_03a_append_specific_indicators")
output_elements_dir = output_base_dir / "Elements"
output_target_layers_dir = output_base_dir / "Target_Layers"


def append_indicators():

    if database_selection == "kbob":
        extract_kbob_data(
            input_dirs=[llm_elements, llm_target_layers], 
            output_base_dir=output_base_dir,
            selected_keys=None
        )
    else:
        extract_oekobaudat_data(
            input_dirs=[llm_elements, llm_target_layers], 
            output_base_dir=output_base_dir, 
            selected_keys=None
        )
    
    append_quantities(
        json_dirs=[output_elements_dir,output_target_layers_dir], boq_path=boq_path
        )

if __name__ == "__main__":
    
    append_indicators()
