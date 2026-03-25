import pandas as pd
import json

# Load and flatten JSON
with open("telemetry1.json") as f:
    data = json.load(f)

df = pd.json_normalize(data, sep='_')

# Keep only numeric columns
df_numeric = df.select_dtypes(include='number')

# Save to CSV
df_numeric.to_csv("output.csv", index=False,header=False)   