# install gffread via conda and activate the enviornment befor running the code
# gffread package -------->  conda install bioconda::gffread
# copy the script in dir of interest and execute -------> python3 filter_transcripts.py 

import pandas as pd
import os
import subprocess
import csv
from Bio import SeqIO

# List of required modules
required_modules = ['pandas', 'SeqIO']

# Function to check if a module is installed
def is_module_installed(module):
    try:
        subprocess.check_output(["pip3", "show", module])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to install a module
def install_module(module):
    subprocess.call(["pip3", "install", module])

# Check and install required modules if not installed
for module in required_modules:
    if not is_module_installed(module):
        print(f"Installing {module}...")
        install_module(module)

# Now all required modules are installed, you can run your code here
print("All required modules are present.")

# input dir of gtf files
dir = "/data/results/sandeep/atharva/samples/cancer_cell_line/breast/nf_core_out/star_salmon/stringtie/transcripts/" 

# path to genome fa
genome = "/data/results/sandeep/atharva/ref/index/genome.fa"

# renaming the files 
file_list = os.listdir(dir)

for file_name in file_list:
    if file_name.endswith('.transcripts.gtf'):
        old_file_path = os.path.join(dir,file_name)
        new_file_name = file_name.replace('.transcripts.gtf', '.gtf')
        new_file_path = os.path.join(dir, new_file_name)
        os.rename(old_file_path, new_file_path)
        print(f"Renames file '{file_name}' to '{new_file_name}'")

# Creating a list of SRA ID for input

file_list = os.listdir(dir)
sra_numbers = [file_name[:-4] for file_name in file_list if file_name.endswith('.gtf')]
print("List of .gtf files without extension:")
print(sra_numbers)

# filtering transcripts based on "transcript" and "reference_id"

for sra_id in sra_numbers:
    gtf = sra_id + ".gtf"
    output_file_name = gtf.replace('.gtf', '_filtered.gtf')
    with open(gtf,'r') as infile, open(output_file_name, 'w') as outfile:
        for i, line in enumerate(infile):
            if i < 2 :
                continue
            columns = line.strip().split('\t')
            if columns[2] != "transcript":
                continue
            if "reference_id" in columns[8]:
                continue
            outfile.write(line) 

# extracting fasta sequences

for sra_id in sra_numbers:
    print ("Extracting sequence for : " + sra_id)
    gffread = "gffread -w" + " " + sra_id + ".fa -g" + " " + genome + " " + sra_id + "_filtered.gtf"
    print ("The command used was:" + gffread)
    subprocess.call(gffread, shell=True)

# counting sequences
output_file_name = "unknown_transcript_counts.txt"

with open(output_file_name, 'w') as outfile:
    for sra_id in sra_numbers:
        fasta_file_name = sra_id + ".fa"
        try:
            count = sum(1 for _ in SeqIO.parse(fasta_file_name, "fasta"))
            print(f"Number of sequences in {fasta_file_name}: {count}")
            outfile.write(f"{fasta_file_name}: {count}\n")
        except FileNotFoundError:
            print(f"File {fasta_file_name} not found.")
            outfile.write(f"File {fasta_file_name} not found.\n")