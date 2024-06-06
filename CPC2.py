import subprocess
import os
import os.path

# input dir of fasta files
dir = "/data/results/sandeep/atharva/samples/cancer_cell_line/breast/nf_core_out/star_salmon/stringtie/transcripts/fasta/" 
out = "/data/results/sandeep/atharva/samples/cancer_cell_line/breast/nf_core_out/star_salmon/stringtie/transcripts/cpc2/"

file_list = os.listdir(dir)
sra_numbers = [file_name[:-3] for file_name in file_list if file_name.endswith('.fa')]
print("List of .fa files without extension:")
print(sra_numbers)

# cpc2

for sra_id in sra_numbers:
    print ("Currently analzings: " + sra_id)
    cpc2 = ("bin/CPC2.py -i" + dir + sra_id + ".fa" + " " + "-o" + out + "cpc_" + sra_id )
    print ("Running the command:" + cpc2)
    subprocess.call(cpc2, shell=True)

# filtering long noncoding RNAs
# Process each file
for sra_id in sra_numbers:
    print ("Currently filtering: " + sra_id)
    filter =  " awk -F'\t' 'NR>1 && $8  ~ /noncoding/ {print$1}'" + " " + "cpc_" + sra_id + ".txt" + " " + " > " + "ID_" + sra_id + ".txt" 
    print ("The command used was: " + filter)
    subprocess.call(filter, shell=True)