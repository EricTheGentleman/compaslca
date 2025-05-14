from methods.utils import append_id
from methods.summarize_results import summarize_inferences
from pathlib import Path

# Master config path
master_config = Path("config/master_config.yaml")

# Root folders of all (step-wise) inferences
inference_root_elements = Path("data/pipeline/step_02_material_matching/step_02a_inference/Elements")
inference_root_target_layers = Path("data/pipeline/step_02_material_matching/step_02a_inference/Target_Layers")

# Root folders of all unfiltered source files
source_root_elements = Path("data/pipeline/step_01_data_extraction/step_01c_dissect_layers/Elements")
source_root_target_layers = Path("data/pipeline/step_01_data_extraction/step_01c_dissect_layers/Target_Layers")

# Output folders for summaries
output_elements = Path("data/pipeline/step_02_material_matching/step_02b_bookkeeping/Elements")
output_target_layers = Path("data/pipeline/step_02_material_matching/step_02b_bookkeeping/Target_Layers")

def bookkeeper():

    # summarize inferences
    summarize_inferences(inference_root_elements, output_elements, master_config)
    summarize_inferences(inference_root_target_layers, output_target_layers, master_config)

    # Append GroupId or GlobalId to inference files for overview
    append_id(output_elements, source_root_elements)
    append_id(output_target_layers, source_root_target_layers)

if __name__ == "__main__":
    bookkeeper()

# IMPORTANT: APPEND MODEL AND PARAMETERS USED!!!