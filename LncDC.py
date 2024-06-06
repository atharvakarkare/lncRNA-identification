import subprocess
import os
import os.path

# input dir of fasta files
dir = "/data/results/sandeep/atharva/samples/cancer_cell_line/breast/nf_core_out/star_salmon/stringtie/transcripts/fasta/" 
out = "/data/results/sandeep/atharva/samples/cancer_cell_line/breast/nf_core_out/star_salmon/stringtie/transcripts/lncdc/"

file_list = os.listdir(dir)
sra_numbers = [file_name[:-3] for file_name in file_list if file_name.endswith('.fa')]
print("List of .fa files without extension:")
print(sra_numbers)

# LncDC

for sra_id in sra_numbers:
    print ("Currently analzings: " + sra_id)
    lncdc = "python3 /data/results/sandeep/atharva/LncDC/bin/lncDC.py -i" + dir + sra_id + ".fa" + " " +"-o " + out + sra_id + ".csv" + " " + "-t -1" 
    print ("Running the command:" + lncdc)
    subprocess.call(lncdc, shell=True)    

# filtering long noncoding RNAs 
# Process each file
for sra_id in sra_numbers:
    print ("Currently filtering: " + sra_id)
    filter = " awk -F',' 'NR > 1 && $26 ~ /lncrna/ {print $1}' " + sra_id + ".csv" + " " + ">" + " " + "id_" + sra_id + ".txt"
    print ("The command used was: " + filter)
    subprocess.call(filter, shell=True)

