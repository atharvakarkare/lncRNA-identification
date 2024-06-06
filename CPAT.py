import subprocess
import os
import os.path
import wget
import pandas as pd

# input dir of gtf files
dir = "/data/results/sandeep/atharva/samples/cancer_cell_line/breast/nf_core_out/star_salmon/stringtie/transcripts/" 


# Creating a list of SRA ID for input

file_list = os.listdir(dir)
sra_numbers = [file_name[:-4] for file_name in file_list if file_name.endswith('.gtf')]
print("List of .gtf files without extension:")
#print(sra_numbers)

# CPAT
url = "https://sourceforge.net/projects/rna-cpat/files/prebuilt_models/Human_logitModel.RData/download"
output_file = "Human_logitModel.RData"

if not os.path.exists(output_file):
    try:
        wget.download(url, out=output_file)
        print("File downloaded successfully!")
    except Exception as e:
        print("Failed to download file:", e)
else:
    print("Human_logitModel.RData exists in the directory.")


url = "https://sourceforge.net/projects/rna-cpat/files/prebuilt_models/Human_Hexamer.tsv/download"
output_file = "Human_Hexamer.tsv"

if not os.path.exists(output_file):
    try:
        wget.download(url, out=output_file)
        print("File downloaded successfully!")
    except Exception as e:
        print("Failed to download file:", e)
else:
    print("Human_Hexamer.tsv exists in the directory.")

subprocess.call('mkdir cpat', shell=True)

for sra_id in sra_numbers:
    print ("Currently analzings: " + sra_id)
    cpat = "cpat -x Human_Hexamer.tsv --antisense -d Human_logitModel.RData --top-orf=5 --min-orf=200 -g" + " " + "/data/results/sandeep/atharva/samples/cancer_cell_line/breast/nf_core_out/star_salmon/stringtie/transcripts/" + sra_id + ".fa -o" + " " + "/data/results/sandeep/atharva/samples/cancer_cell_line/breast/nf_core_out/star_salmon/stringtie/transcripts/cpat/" + sra_id + " " + "--verbose"
    print ("Running the command:" + cpat)
    subprocess.call(cpat, shell=True)



