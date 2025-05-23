import json
from pathlib import Path

# Emission keys for KBOB
ENV_KEYS_KBOB = [
    "Global Warming Potential Total [kgCO2-eqv]",
    "Global Warming Potential Manufacturing [kgCO2-eqv]",
    "Global Warming Potential Disposal [kgCO2-eqv]",
    "Biogenic Carbon [kg C]",
    "UBP (Total)",
    "UBP (Manufacturing)",
    "UBP (Disposal)",
    "Total Renewable Primary Energy [kWh oil-eq]",
    "Manufacturing Renewable Primary Energy [kWh oil-eq]",
    "Disposal Renewable Primary Energy [kWh oil-eq]",
    "Total Non-Renewable Primary Energy [kWh oil-eq]",
    "Manufacturing Non-Renewable Primary Energy [kWh oil-eq]",
    "Disposal Non-Renewable Primary Energy [kWh oil-eq]"
]

# Emission keys for OEKOBAUDAT
ENV_KEYS_OEKOBAUDAT = [
    "GWPtotal (A1)", "GWPtotal (A2)", "GWPtotal (A3)", "GWPtotal (A1-A3)",
    "GWPtotal (A4)", "GWPtotal (A5)", "GWPtotal (B1)", "GWPtotal (B2)",
    "GWPtotal (B3)", "GWPtotal (B4)", "GWPtotal (B5)", "GWPtotal (B6)",
    "GWPtotal (B7)", "GWPtotal (C1)", "GWPtotal (C2)", "GWPtotal (C3)",
    "GWPtotal (C4)", "GWPbiogenic", "GWPfossil", "GWPtotal"
]

def determine_multiplier(material, volume, area):
    ref = material.get("Reference", "").lower()
    if ref == "kg":
        return float(material.get("Density (kg/m3)", 1)) * float(volume)
    elif ref == "qm":
        return float(area)
    elif ref == "m3":
        return float(volume)
    elif ref == "pcs":
        return 1
    else:
        return 1 

def process_material(material, volume, area, keys):
    multiplier = determine_multiplier(material, volume, area)
    for key in keys:
        if key in material:
            try:
                value = float(material[key])
                material[key] = str(round(value * multiplier, 4))
            except ValueError:
                pass
    return material


def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    volume = data.get("Volume [m^3]", 1)
    area = data.get("Largest Surface Area [m^2]", 1)

    # Handle both KBOB and OEKOBAUDAT formats
    if "Matched Materials with KBOB Indicators" in data:
        key = "Matched Materials with KBOB Indicators"
        new_key = "Matched Materials with Gross Emissions (KBOB)"
        emission_keys = ENV_KEYS_KBOB
    elif "Matched Materials with OEKOBAUDAT Indicators" in data:
        key = "Matched Materials with OEKOBAUDAT Indicators"
        new_key = "Matched Materials with Gross Emissions (OEKOBAUDAT)"
        emission_keys = ENV_KEYS_OEKOBAUDAT
    else:
        return  # skip files without expected data

    materials = data.pop(key, [])
    processed = [process_material(m, volume, area, emission_keys) for m in materials]
    data[new_key] = processed

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def calculate_gross_emissions(input_dirs, output_base_dir):
    output_base_path = Path(output_base_dir)

    for input_dir in input_dirs:
        input_dir_path = Path(input_dir)
        input_dir_name = input_dir_path.name
        output_subdir = output_base_path / input_dir_name
        output_subdir.mkdir(parents=True, exist_ok=True)

        for json_file in input_dir_path.glob("*.json"):
            original_name = json_file.name

            if original_name.endswith("_indicators.json"):
                new_filename = original_name.replace("_indicators.json", "_emissions.json")
            else:
                new_filename = original_name

            output_path = output_subdir / new_filename
            process_file(json_file, output_path)
