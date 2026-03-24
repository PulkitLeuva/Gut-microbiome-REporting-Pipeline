# GREP (Gut-microbiome REporting Pipeline)

## 🧬 Summary

This repository contains a fully automated Snakemake pipeline for gut microbiome analysis.

---

### 🔄 Clone This Repository

```bash
git clone https://github.com/PulkitLeuva/Gut-microbiome-REporting-Pipeline.git
cd Gut-microbiome-REporting-Pipeline
```
## 🛠️ Installation Guide

### 1. Install Miniconda (if not already installed)

Follow the official instructions: https://docs.conda.io/en/latest/miniconda.html

Or use this command (Linux):

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
```bash
bash Miniconda3-latest-Linux-x86_64.sh
```
Create New conda environment using given yml file
```bash
conda env create -f envs/gut_snakemake_env.yml
```
Activate the new environment
```bash
conda activate gut_microbiome_env
```
Please change the config file to update the base directory path. Use the repo directory folder for path.
Also you need to download the reference genome (Homo_sapiens_hg37_and_human_contamination_Bowtie2_v0.1) from this link https://huttenhower.sph.harvard.edu/kneadData_databases/.
Run Snakemake pipeline using below command if your conda uses default solver
```bash
snakemake --cores all --use-conda all
```
Run Snakemake pipeline using this command if your conda uses mamba solver
```bash
snakemake --cores 1 --use-conda --conda-frontend conda all
```
When ran for the first time the pipeline may take time to download metaphlan database.
