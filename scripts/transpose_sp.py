import pandas as pd

# Read the Excel file
df = pd.read_excel("/lustre/pulkit.h/snakemake_local/gut_microbiome_automation/snakemake/output/metaphlan/0BPXYV_species.xlsx")
print(df)
# Extract sample ID from the first column
sample_id = df.iloc[0, 0]

# Drop the first column (Unnamed: 0), keep only species columns
species_abundance = df.drop(columns=df.columns[0])

# Transpose the DataFrame
df_transposed = species_abundance.T

# Add species names and relative abundance as columns
df_transposed.reset_index(inplace=True)
df_transposed.columns = ['Species', str(sample_id)]

print(df_transposed)
#df_transposed.to_csv("/lustre/pulkit.h/snakemake_local/gut_microbiome_automation/snakemake/output/metaphlan/0BPXYV_species.xlsx")