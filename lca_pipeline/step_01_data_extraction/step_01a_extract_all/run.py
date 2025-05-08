import time
from pathlib import Path
from methods.extractor import extractor
from methods.extractor_boq import extractor_boq
from methods.helpers_io import load_ifc_file, load_yaml_config, get_single_ifc_file

def extract_all():

    start_time = time.time()

    brep_toggle = True

    # Input, output and config paths
    input_file = str(get_single_ifc_file())
    out_directory_compositions = Path("data/pipeline/step_01_data_extraction/step_01a_extract_all/Compositions")
    out_directory_elements = Path("data/pipeline/step_01_data_extraction/step_01a_extract_all/Elements")
    out_directory_boq = Path("data/pipeline/step_01_data_extraction/step_01a_extract_all")
    config_path = Path("config/step_01_data_extraction/extraction_config.yaml")
    master_config_path = Path("config/master_config.yaml")

    # Load the extraction configuration from a YAML file
    config = load_yaml_config(config_path)
    master_config = load_yaml_config(master_config_path)

    # Read geometry settings
    extraction_config = master_config.get("extraction_config", {})
    max_elements = extraction_config.get("max_elements", None)
    brep_toggle = extraction_config.get("brep_enabled", True)
    brep_timeout = extraction_config.get("brep_timeout", 30)

    try:
        # Load the IFC file
        model = load_ifc_file(input_file)

        # Extract element data and save each IfcBuildingElement separately
        extractor(brep_toggle, brep_timeout, input_file, model, out_directory_elements, out_directory_compositions, out_directory_boq, max_elements, config)

        # Append elements to to BoQ
        extractor_boq(out_directory_elements, out_directory_boq)

        # Stop measuring time
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"All elements extracted in {elapsed_time:.2f} seconds.")

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    extract_all()