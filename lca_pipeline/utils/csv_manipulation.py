import pandas as pd

# Load both CSV files with UUIDs as strings, avoid dtype issues
df_ref = pd.read_csv('data/input/LCI_database/csv/oekobaudat.csv', dtype={'UUID': str})
df_target = pd.read_csv('data/input/LCI_database/csv/oekobaudat_indicators.csv', dtype={'UUID': str}, low_memory=False)

# Normalize UUIDs: strip spaces, lowercase, remove hidden BOM characters
df_ref['UUID'] = df_ref['UUID'].astype(str).str.strip().str.replace('\ufeff', '', regex=False).str.lower()
df_target['UUID'] = df_target['UUID'].astype(str).str.strip().str.replace('\ufeff', '', regex=False).str.lower()

# Create set of valid UUIDs
valid_uuids = set(df_ref['UUID'])

# Debug print: show UUIDs and overlap
print(f"REF UUIDs: {len(df_ref['UUID'].unique())}")
print(f"TARGET UUIDs: {len(df_target['UUID'].unique())}")

# Create sets
set_ref = set(df_ref['UUID'])
set_target = set(df_target['UUID'])

# Show overlaps and mismatches
overlap = set_ref.intersection(set_target)
only_in_target = set_target - set_ref
only_in_ref = set_ref - set_target

print(f"→ Overlap: {len(overlap)} UUIDs")
print(f"→ UUIDs in target not in ref: {len(only_in_target)}")
print(f"→ UUIDs in ref not in target: {len(only_in_ref)}")

# Optional: print some examples
print("Sample unmatched UUIDs in target:", list(only_in_target)[:5])


# Filter the target file based on reference UUIDs
filtered_df = df_target[df_target['UUID'].isin(valid_uuids)]

# Save the filtered DataFrame
filtered_df.to_csv('data/input/LCI_database/csv/oekobaudat_indicators_update.csv', index=False)

print(f"Filtered {len(df_target) - len(filtered_df)} rows. Output saved to 'oekobaudat_indicators_update.csv'.")

