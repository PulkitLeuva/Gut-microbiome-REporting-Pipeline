import subprocess
import utils
import os
import pandas as pd
from joblib import load
import numpy as np
from time import sleep
import traceback
from halo import Halo
import gzip
import zipfile
import shutil
import sys

success = u"\u2705"
fail = u"\u274C"
poop = u"\U0001F4A9"
spin = "line"
party1 = u"\U0001F973"
party2 = u"\U0001F389"

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


spin = "line"
def printw(s):
   print(bcolors.WARNING + s + bcolors.ENDC)

def printg(s):
   print(bcolors.BOLD + bcolors.OKGREEN + s + bcolors.ENDC)
   
def printr(s):
   print(bcolors.BOLD + bcolors.FAIL + s + bcolors.ENDC)

def rm_r(path):
  if os.path.isdir(path) and not os.path.islink(path):
      shutil.rmtree(path)
  elif os.path.exists(path):
      os.remove(path)

def profile(args):
  spinner = Halo(text='Profiling metagenome', spinner=spin)
  spinner.start()

  command = [
    "metaphlan",
    f"{args}_R1_paired_trim.fastq.gz,{args}_R1_paired_trim.fastq.gz",
    "--index", 
    "mpa_v30_CHOCOPhlAn_201901",
    "--force",
    "--no_map",
    "--input_type",
    "fastq",
    "-o",
    args + "_metaphlan.txt",
    "--add_viruses",
    "--unknown_estimation",
  ]
  proc = subprocess.Popen(command, stderr=subprocess.PIPE)
  stderr = proc.stderr.read().decode("utf-8") 
  proc.communicate()

  if proc.returncode == 0:
    spinner.succeed()
  else:
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    sys.exit()

  rm_r(f"{args}_R1_paired_trim.fastq.gz")
  rm_r(f"{args}_R1_paired_trim.fastq.gz")

def microbiome_analysis(args,out1,out2):
  print(
        "-" * 10,
        "Microbiome analysis",
        "-" * 10,
  )
  #profile(args)    
  spinner = Halo(text='Computing GMWI2', spinner=spin)
  spinner.start()

  gmwi2_error = None
  try:
    compute_gmwi2(args,out1,out2)
  except Exception as e:
    gmwi2_error = traceback.format_exc()

  if gmwi2_error:
    spinner.fail()
    printw(gmwi2_error)
    printr("GMWI2 aborted " + poop)
    sys.exit()
  else:
    spinner.succeed()

  print(
        "-" * 41,
        "\n"
  )

def compute_gmwi2(args,out1,out2):
    # Load in taxonomic profile
    df = pd.read_csv(args, sep="\t", skiprows=3, usecols=[0, 2], index_col=0).T
    
    # Ensure all data is numeric
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)  # Convert to numeric and fill NaN with 0

    # Load model
    gmwi2 = load(os.path.join(utils.DEFAULT_DB_FOLDER, "GMWI2_model.joblib"))

    # Identify dummy columns
    dummy_cols = list(set(gmwi2.feature_names_in_) - set(df.columns))
    dummy_df = pd.DataFrame(np.zeros((1, len(dummy_cols))), columns=dummy_cols, index=["relative_abundance"])
    df = pd.concat([dummy_df, df], axis=1)

    # Check for 'UNKNOWN' column and handle accordingly
    if 'UNKNOWN' in df.columns:
        # Normalize relative abundances
        df = df.divide((100 - df["UNKNOWN"]), axis="rows")
        # Drop the 'UNKNOWN' column
        df = df.drop(labels=["UNKNOWN"], axis=1)
    else:
        # If 'UNKNOWN' column is not present, normalize without it
        total_abundance = df.sum(axis=1).values[0]  # Get the total of all other taxa
        if total_abundance > 0:  # Check if total abundance is greater than 0
            df = df.divide(total_abundance, axis="rows")
        else:
            print("Warning: Total abundance is zero. Skipping normalization.")

    # Ensure df has the same columns and order as the model
    df = df.reindex(columns=gmwi2.feature_names_in_, fill_value=0)

    # Compute GMWI2
    presence_cutoff = 0.00001
    score = gmwi2.decision_function(df > presence_cutoff)[0]

    # Write results to file
    with open(out1, "w") as f:
        f.write(f"{score}\n")

    # Record relative taxa that are present and have nonzero coef in model
    coefficient_df = pd.DataFrame(gmwi2.coef_, columns=gmwi2.feature_names_in_, index=["coefficient"]).T
    coefficient_df["relative_abundance"] = df.values.flatten()
    coefficient_df = coefficient_df[(coefficient_df["coefficient"] != 0) & (coefficient_df["relative_abundance"] > presence_cutoff)]
    coefficient_df.index.name = "taxa_name"
    coefficient_df = coefficient_df[["coefficient"]]

    coefficient_df.to_csv(out2, sep="\t")


def cleanup(args):
  intermediate = [
    # "QC_1P.fastq.gz",
    # "QC_1U.fastq.gz",
    # "QC_2P.fastq.gz",
    # "QC_2U.fastq.gz",
    # "adapter1.txt",
    # "adapter2.txt",
    # "adapters.txt",
    # "human.bam",
    # "human1.fastq",
    # "human2.fastq",
    # "human_sorted.bam",
    # "in1.fastq",
    # "in2.fastq",
    # "mapped.bam",
    # "mapped.sam",
    # "repaired1.fastq",
    # "repaired1_fastqc",
    # "repaired1_fastqc.html",
    # "repaired2.fastq",
    # "repaired2_fastqc",
    # "repaired2_fastqc.html",
  ]

  intermediate = [f"{args}_{i}" for i in intermediate]

  for f in intermediate:
    # don't accidentally delete input files! 
    # For the case where an intermediate file has the same name as an input file
    if f == args.forward or f == args.reverse:
      continue

    rm_r(f)

def run(args,out1,out2):
  #dependency_checks()
  #database_installation()
  #quality_control(args)
  microbiome_analysis(args,out1,out2)
  #cleanup(args)

  printg("GMWI2 great success!" + poop + party1 + party2)


input_file = sys.argv[1]
output_file1 = sys.argv[2]
output_file2 = sys.argv[3]

#file = "/lustre/rohan.b/Gut_Mcrobiome_sequencing_runs/gmwi2_tool/GMWI2/src/GMWI2/input/2KLK3C_S165"
#input_file = "/lustre/pulkit.h/snakemake_local/gut_microbiome_automation/GMWI2/example/SRR1761667"
run(input_file,output_file1,output_file2)