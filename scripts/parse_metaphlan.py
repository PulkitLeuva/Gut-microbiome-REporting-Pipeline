import pandas as pd
from io import StringIO

# Get input and output paths from Snakemake
input_file = snakemake.input[0]
output_file_ph = snakemake.output.phylum
output_file_sp = snakemake.output.species
output_count = snakemake.output.count_file

# Extract sample ID from input filename
sample_id = input_file.split("/")[-1].replace("_profiled_mpa4.txt", "")

# Read MetaPhlAn output
df = pd.read_csv(input_file, sep='\t', comment='#', header=None,
                 names=["clade_name", "NCBI_tax_id", "relative_abundance", "additional_species"],
                 usecols=["clade_name", "relative_abundance"])

# Filter for bacterial species
species_df = df[df['clade_name'].str.contains(r"\|s__") & df['clade_name'].str.startswith("k__Bacteria")].copy()

# Split taxonomy
tax_split = species_df['clade_name'].str.split('|', expand=True)
tax_split.columns = ['Domain','Phylum','Class','Order','Family','Genus','Species','Strain']
species_df = species_df.assign(**tax_split)

# ---- PHYLUM-LEVEL ----
phylum_df = species_df.copy()
phylum_grouped = (
    phylum_df.groupby('Phylum')['relative_abundance']
    .sum()
    .reset_index(name='rel_abund')
)
phylum_grouped['value'] = phylum_grouped['rel_abund'] * 100 / phylum_grouped['rel_abund'].sum()
phylum_out = phylum_grouped[['Phylum', 'value']].set_index('Phylum').T
phylum_out.index = [sample_id]

# ---- SPECIES-LEVEL ----
species_grouped = (
    species_df.groupby('Species')['relative_abundance']
    .sum()
    .reset_index(name='rel_abund')
)
species_grouped['value'] = species_grouped['rel_abund'] * 100 / species_grouped['rel_abund'].sum()
species_out = species_grouped[['Species', 'value']].set_index('Species').T
species_out.index = [sample_id]

# 🔹 Remove prefixes like "p__" and "s__"
phylum_out.columns = phylum_out.columns.str.replace("p__", "", regex=False)
species_out.columns = species_out.columns.str.replace("s__", "", regex=False)

# Write to CSV
phylum_out.to_csv(output_file_ph)
species_out.to_csv(output_file_sp)

print(f"✅ Wrote phylum output to {output_file_ph}")
print(f"✅ Wrote species output to {output_file_sp}")

# Get sample name from file name
#sample_name = os.path.basename(species_file).replace("_species.csv", "")

# Read CSVs
species_df = species_out
phylum_df = phylum_out

# Count non-zero relative abundances (i.e., detected taxa)
species_count = (species_df.iloc[0] > 0).sum()
phylum_count = (phylum_df.iloc[0] > 0).sum()

# Create output DataFrame
summary_df = pd.DataFrame([{
    "Sample": sample_id,
    "Species_count": species_count,
    "Phylum_count": phylum_count
}])

# Save to CSV
summary_df.to_csv(output_count, index=False)