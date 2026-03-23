# scripts/install_packages.R

packages <- c("ecotraj","devtools","writexl","ggbiplot","ggpubr",
              "vegan","ggtext","tidytext","tidyverse","xlsx","openxlsx")

cran_mirror <- "https://cran.r-project.org"

install_if_missing <- function(pkg) {
  if (!require(pkg, character.only = TRUE)) {
    message(paste("Installing package:", pkg))
    tryCatch({
      install.packages(pkg, repos = cran_mirror)
      if (!require(pkg, character.only = TRUE)) {
        stop(paste("Failed to install package:", pkg))
      }
    }, error = function(e) {
      message(paste("Error installing package", pkg, ":", e$message))
    })
  } else {
    message(paste("Package already installed:", pkg))
  }
}

invisible(lapply(packages, install_if_missing))