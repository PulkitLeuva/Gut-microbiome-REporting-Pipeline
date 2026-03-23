library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)
score_file <- args[1]        # e.g., "output/0BPXYV_gmwi2_score.txt"
output_plot <- args[2]       # e.g., "output/0BPXYV_gmwi2_score_plot.png"
csv_output <- args[3]        # e.g., "output/0BPXYV_metadata.csv"

# === Extract sample ID ===
sample_id <- basename(score_file)
sample_id <- sub("_gmwi2_score\\.txt$", "", sample_id)

# === Read the GMWI2 score ===
wellness_value <- as.numeric(readLines(score_file, warn = FALSE))

# === Save CSV with cleaned sample ID ===
gmwi2_df <- data.frame(Sample = sample_id, GMWI2 = wellness_value)
write.csv(gmwi2_df, csv_output, row.names = FALSE, quote = TRUE)

# === Plot the GMWI2 score ===
plot <- ggplot() +
  geom_segment(aes(x = -5, xend = 5, y = 0, yend = 0), color = "grey80", size = 1.5) +
  geom_point(aes(x = wellness_value, y = 0),
             color = ifelse(wellness_value > 0, "#81C784",
                            ifelse(wellness_value < 0, "#FF6F6F", "#F6C357")),
             size = 7) +
  scale_x_continuous(limits = c(-5, 5), breaks = seq(-5, 5, by = 1)) +
  scale_y_continuous(limits = c(-1, 1), breaks = NULL) +
  theme_classic() +
  labs(x = paste("\nYour Wellness Score =", round(wellness_value, 2)),
       y = "",
       title = "") +
  theme(
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.text.x = element_text(size = 12),
    plot.title = element_text(size = 14, hjust = 0.5),
    aspect.ratio = 0.07
  )

# === Save the plot ===
ggsave(filename = output_plot, plot = plot, width = 7, height = 1.5)