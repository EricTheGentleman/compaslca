import os
import subprocess

# Define the pipeline steps with custom keys
MODULES = [
    {"key": "a", "name": "Step 01: Data Extraction", "path": "lca_pipeline/step_01_data_extraction/run.py"},
    {"key": "b", "name": "Step 01c: Dissect Layers", "path": "lca_pipeline/step_01c_dissect_layers/run.py"},
    {"key": "c", "name": "Step 01d: Filter Data", "path": "lca_pipeline/step_01d_filter_data/run.py"},
    {"key": "d", "name": "Step 02: BoQ Generation", "path": "lca_pipeline/step_02_boq_generation/run.py"},
]

def run_module(module):
    print(f"\n🔧 Running module: {module['name']}")
    try:
        subprocess.run(["python", module["path"]], check=True)
        print(f"✅ Finished: {module['name']}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {module['name']}: {e}")

def pipeline_menu():
    while True:
        print("\n======================")
        print("🚀 COMPAS_LCA PIPELINE")
        print("======================")
        print("Select a module to run:")

        for mod in MODULES:
            print(f"  {mod['key'].upper()}. {mod['name']}")

        print("  R. Run all modules sequentially")
        print("  Q. Quit")

        choice = input("\nYour choice: ").strip().lower()

        if choice == "q":
            print("👋 Exiting.")
            break

        elif choice == "r":
            for mod in MODULES:
                run_module(mod)
                input("➡️  Press Enter to continue to the next module...")
            print("✅ All modules completed.\n")

        elif choice in [mod["key"] for mod in MODULES]:
            selected = next(mod for mod in MODULES if mod["key"] == choice)
            run_module(selected)
            input("➡️  Press Enter to return to the menu...")

        else:
            print("❗ Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    pipeline_menu()
