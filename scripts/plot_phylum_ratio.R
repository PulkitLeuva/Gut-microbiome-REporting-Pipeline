# Load required libraries
library(readxl)
library(tidyverse)
library(glue)

# === Input arguments ===
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]         # e.g., "output/metaphlan/0BPXYV_phylum.xlsx"
output_file <- args[2]        # e.g., "output/metaphlan/0BPXYV_ratio.png"
ratio_output_file <- args[3]  # e.g., "output/metaphlan/0BPXYV_ratio.txt"

# === Read the phylum data ===
df <- read.csv(input_file, check.names = FALSE)
df <- as.data.frame(df)

# Get sample ID
sample_id <- df[[1]]
df_long <- df %>%
  select(-1) %>%
  pivot_longer(cols = everything(), names_to = "Phylum", values_to = "value") %>%
  filter(value > 0)

# Extract Firmicutes and Bacteroidetes (MetaPhlAn4 calls Bacteroidetes "Bacteroidota")
firmicutes_abundance <- df_long %>% 
  filter(Phylum == "Firmicutes") %>% 
  pull(value) %>% 
  sum()

bacteroidetes_abundance <- df_long %>% 
  filter(Phylum == "Bacteroidota") %>% 
  pull(value) %>% 
  sum()

# Create data frame for plotting
phyla_data <- data.frame(
  Phylum = c("Firmicutes", "Bacteroidota"),
  Abundance = c(firmicutes_abundance, bacteroidetes_abundance)
)

# Compute ratio
ratio_f_b <- firmicutes_abundance / bacteroidetes_abundance
title_text <- ifelse(ratio_f_b > 10, ">10", round(ratio_f_b, 2))

# Save ratio value to file
# Extract sample name (assumes file name like "output/metaphlan/abc123_phylum.csv")
sample_name <- tools::file_path_sans_ext(basename(input_file)) %>%
  str_replace("_phylum", "")

# Save ratio value to CSV
ratio_df <- data.frame(Sample = sample_name, `F/B` = round(ratio_f_b, 2))
write.csv(ratio_df, ratio_output_file, row.names = FALSE)

# Create pie chart
pie_chart <- ggplot(phyla_data, aes(x = "", y = Abundance, fill = Phylum)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar(theta = "y") +
  labs(
    title = glue("F / B = {title_text}"),
    fill = "Phylum"
  ) +
  theme_void() +
  theme(
    legend.position = "right",
    plot.title = element_text(size = 25, face = "bold", hjust = 0.5),
    legend.text = element_text(size = 18, face = "bold"),
    legend.title = element_text(size = 20, face = "bold")
  ) +
  scale_fill_manual(values = c("Firmicutes" = "#FF6666", "Bacteroidota" = "#FFB266")) +
  geom_text(
    aes(label = paste0(sprintf("%.2f%%", Abundance / sum(Abundance) * 100))),
    position = position_stack(vjust = 0.5),
    size = 7.5
  )

# Save plot
ggsave(filename = output_file, plot = pie_chart, height = 5, width = 8, dpi = 600)