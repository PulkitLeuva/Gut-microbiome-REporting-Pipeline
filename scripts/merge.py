import pandas as pd
import sys

# === Input CSV file paths ===
csv1 = sys.argv[1]  # e.g., "output/sample1_diversity.csv"
csv2 = sys.argv[2]  # e.g., "output/sample1_firmicutes_bacteroidota_ratio.csv"
csv3 = sys.argv[3]  # e.g., "output/sample1_gmwi2.csv"
csv4 =sys.argv[4]
output_file = sys.argv[5]  # e.g., "output/sample1_metadata_combined.csv"

# === Read each CSV ===
df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)
df3 = pd.read_csv(csv3)
df4 = pd.read_csv(csv4)
# === Merge on 'Sample' column ===
merged_df = df1.merge(df2, on="Sample", how="outer")
merged_df = merged_df.merge(df3, on="Sample", how="outer")
merged_df = merged_df.merge(df4, on="Sample", how="outer")
# === Save final merged metadata ===
merged_df.to_csv(output_file, index=False)