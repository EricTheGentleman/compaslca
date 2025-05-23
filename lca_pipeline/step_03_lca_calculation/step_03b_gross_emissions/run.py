from methods.multiply import calculate_gross_emissions
from pathlib import Path

"""
element_indicators = Path("data/pipeline/step_03_lca_calculation/step_03a_append_specific_indicators/Elements")
target_layer_indicators = Path("data/pipeline/step_03_lca_calculation/step_03a_append_specific_indicators/Target_Layers")
output_base_dir = Path("data/pipeline/step_03_lca_calculation/step_03b_gross_emissions")
"""
element_indicators = Path("data/pipeline/step_03_lca_calculation/step_03a_append_specific_indicators/z_test_Oekobaudat/Elements")
target_layer_indicators = Path("data/pipeline/step_03_lca_calculation/step_03a_append_specific_indicators/z_test_Oekobaudat/Target_Layers")
output_base_dir = Path("data/pipeline/step_03_lca_calculation/step_03b_gross_emissions/z_test_Oekobaudat")

if __name__ == "__main__":
    
    calculate_gross_emissions(input_dirs=[element_indicators, target_layer_indicators], output_base_dir=output_base_dir)