library(readxl)
library(dplyr)
library(glue)
library(writexl)
library(tibble)

args <- commandArgs(trailingOnly = TRUE)
top20_file <- args[1]
new_updated_file <- args[2]
species_file <- args[3]
output_file <- args[4]

# Load top 20 species
top20 <- read_excel(top20_file) %>% 
  distinct(Species)

# Load updated species info (SCFA + description)
updated_list <- read_excel(new_updated_file) %>% 
  distinct(Species, Scfa_produced, Description)

# Merge: enrich top 20 with SCFA + description if available
final_ben <- updated_list %>%
  left_join(top20, by = "Species")

# Load horizontal species abundance table (one row, species as columns)
raw_species <- read.csv(species_file, check.names = FALSE)

# Transpose: turn horizontal into vertical and fix species naming
sample_table <- tibble(
  Species = gsub("_", " ", names(raw_species)),  # 🛠 fix underscores
  value = as.numeric(raw_species[1, ])
)

# Find matches (present species)
sample_ben <- final_ben %>%
  inner_join(sample_table, by = "Species")

# Annotate presence
sample_ben_final <- final_ben %>%
  left_join(sample_ben, by = "Species") %>%
  mutate(Presence = if_else(!is.na(value), "+", "-")) %>%
  arrange(desc(value))

# Clean final output
final_beneficial <- sample_ben_final %>%
  transmute(
    Species,
    Presence,
    Scfa_produced = coalesce(Scfa_produced.x, "Not available"),
    Description = coalesce(Description.x, "Not available")
  )

# Write final table
write.csv(final_beneficial, output_file, row.names = FALSE)