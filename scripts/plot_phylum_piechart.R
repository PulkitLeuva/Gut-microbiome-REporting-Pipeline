# Load required libraries
library(readxl)
library(tidyverse)
library(glue)

# === Input arguments ===
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]   # e.g., "output/metaphlan/0BPXYV_phylum.xlsx"
output_file <- args[2]  # e.g., "output/metaphlan/0BPXYV_phylum.png"

# === Read the phylum data ===
df <- read.csv(input_file, check.names = FALSE)
df <- as.data.frame(df)

# Get sample ID (assuming first column is sample ID and there's only one row)
sample_id <- df[[1]]
df_long <- df %>%
  select(-1) %>%
  pivot_longer(cols = everything(), names_to = "Phylum", values_to = "value") %>%
  filter(value > 0) %>%
  mutate(percentage = value / sum(value) * 100)

# Prepare legend labels
df_long <- df_long %>%
  mutate(rounded_percentage = ifelse(percentage < 0.01, "< 0.01", sprintf("%.2f", percentage))) %>%
  mutate(label = glue("{Phylum} ({rounded_percentage}%)"))

# Order phyla
p_order <- df_long$Phylum

# Plot
p <- df_long %>%
  mutate(Phylum = factor(Phylum, levels = p_order)) %>%
  ggplot(aes(x = "", y = value, fill = Phylum)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar(theta = "y", direction = 1) +
  labs(title = NULL, fill = "Phyla") +   # <- no title
  theme_void() +
  theme(legend.position = "right") +
  scale_fill_manual(values = scales::hue_pal()(length(p_order)),
                    labels = df_long$label)

# Save plot
ggsave(output_file, plot = p, height = 4, width = 5, dpi = 300)