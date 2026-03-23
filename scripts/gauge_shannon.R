library(tidyverse)
library(glue)
library(ggplot2)

# Function to create the semi-circular gauge plot
create_semi_circular_gauge <- function(
  value, max_value, title, filename,
  num_labels = 4
) {
  gauge_start_angle_deg <- 180
  gauge_end_angle_deg <- 0
  
  gauge_start_angle <- gauge_start_angle_deg * pi / 180
  gauge_end_angle <- gauge_end_angle_deg * pi / 180
  
  limited_value <- min(value, max_value)
  angle <- gauge_start_angle + (limited_value / max_value) * (gauge_end_angle - gauge_start_angle)
  
  # Define breaks and colors tailored for Shannon diversity scale (adjust as needed)
  breaks <- c(0, 1.5, 3.0, 5.0)
  color_breaks <- c("#FF6F6F", "#F6C357", "#81C784")  # Red, Amber, Green
  
  get_poly <- function(a, b, r1=0.7, r2=1.0, n=50) {
    th.start <- gauge_start_angle + (a / max_value) * (gauge_end_angle - gauge_start_angle)
    th.end   <- gauge_start_angle + (b / max_value) * (gauge_end_angle - gauge_start_angle)
    th       <- seq(th.start, th.end, length=n)
    x        <- c(r1 * cos(th), rev(r2 * cos(th)))
    y        <- c(r1 * sin(th), rev(r2 * sin(th)))
    return(data.frame(x, y))
  }
  
  scale_labels <- data.frame(
    angle = c(gauge_start_angle, gauge_end_angle),
    label = c(0, max_value),
    x = c(cos(gauge_start_angle) * 1.1, cos(gauge_end_angle) * 1.1),
    y = c(sin(gauge_start_angle) * 1.1, sin(gauge_end_angle) * 1.1)
  )
  
  p <- ggplot() +
    geom_polygon(data=get_poly(breaks[1], breaks[2]), aes(x, y), fill=color_breaks[1]) +
    geom_polygon(data=get_poly(breaks[2], breaks[3]), aes(x, y), fill=color_breaks[2]) +
    geom_polygon(data=get_poly(breaks[3], breaks[4]), aes(x, y), fill=color_breaks[3]) +
    geom_segment(aes(x = 0, y = 0, xend = cos(angle) * 0.7, yend = sin(angle) * 0.7),
                 color = "black", size = 1, arrow = arrow(type = "open", length = unit(0.2, "cm")), lineend = "round") +
    geom_text(data = scale_labels, aes(x = x, y = y, label = label), size = 5, angle = 0, fontface = "bold", color = "#333333") +
    geom_text(data = data.frame(x = 0, y = -0.1, label = paste0("Score= ", round(value, 2))),
              aes(x = x, y = y, label = label), size = 5, fontface = "bold") +
    coord_fixed() +
    theme_void() +
    theme(plot.margin = margin(0, 0, 0, 0, "cm"))
  
  ggsave(filename = filename, plot = p, width = 4.8, height = 3, dpi = 600)
}

# ---- Main ----
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]

metrics <- read.csv(input_file)

# Extract Shannon diversity for the first sample (adjust if multiple samples)
shannon_value <- metrics$Shannon[1]
sample_name <- metrics$Sample[1]

max_value <- 5.0  # Typical max for Shannon diversity, adjust if needed

output_file <- glue(output_file)

create_semi_circular_gauge(
  value = shannon_value,
  max_value = max_value,
  title = "Shannon Diversity", 
  filename = output_file
)

# message(glue("Shannon diversity gauge plot saved at: {output_file}"))