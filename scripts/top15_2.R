#!/usr/bin/env Rscript

library(readxl)
library(tidyverse)
library(RColorBrewer)

# Get command-line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]

# Read Excel file with column names
data <- read.csv(input_file, check.names = FALSE)

# Extract sample ID (first column value)
sample_id <- data[[1]][1]

# Remove first column (sample ID)
abund_values <- data[1, -1]

# Get species names from column headers
species_names <- colnames(abund_values)

# Create a tidy dataframe
# Create a tidy dataframe
df <- tibble(
  Species = species_names,
  Relative_Abundance = as.numeric(unlist(abund_values))
)
# Filter out NA or zero abundance
df <- df %>%
  filter(!is.na(Relative_Abundance) & Relative_Abundance > 0)

# Select top 15
df_top15 <- df %>%
  arrange(desc(Relative_Abundance)) %>%
  slice_head(n = 15)

# Print for verification
cat("Top 15 most abundant species:\n")
print(df_top15, n = 15)

# Set factor level to preserve order
df_top15$Species <- factor(df_top15$Species, levels = df_top15$Species)

# Define color palette
colors <- c(brewer.pal(12, "Set3"), brewer.pal(7, "Paired"))[1:nrow(df_top15)]

# Plot
p <- ggplot(df_top15, aes(x = Species, y = Relative_Abundance, fill = Species)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  labs(
    #title = paste("Top 15 Most Abundant Species in", sample_id),
    x = "Species", y = "Relative Abundance"
  ) +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 70, hjust = 1)) +
  scale_fill_manual(values = colors)

# Save plot
ggsave(output_file, plot = p, width = 10, height = 6, dpi = 600)