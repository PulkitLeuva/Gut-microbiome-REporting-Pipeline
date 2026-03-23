
library(vegan)
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]
# Example: Read your CSV file
df <- read.csv(input_file, row.names = 1)

# Calculate Richness (number of non-zero species)
richness <- specnumber(df)  # Observed species per sample

# Shannon Diversity
shannon <- diversity(df, index = "shannon")

# Evenness
evenness <- shannon / log(richness)

# Combine into a data frame
diversity_metrics <- data.frame(
  Sample = rownames(df),
  Richness = richness,
  Shannon = shannon,
  Evenness = evenness
)

#print(diversity_metrics)
# Save to CSV
write.csv(diversity_metrics, output_file, row.names = FALSE)