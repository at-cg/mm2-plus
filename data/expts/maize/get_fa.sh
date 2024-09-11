# Get maize genome
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/022/117/705/GCA_022117705.1_Zm-Mo17-REFERENCE-CAU-T2T-assembly/GCA_022117705.1_Zm-Mo17-REFERENCE-CAU-T2T-assembly_genomic.fna.gz

gunzip GCA_022117705.1_Zm-Mo17-REFERENCE-CAU-T2T-assembly_genomic.fna.gz

mv GCA_022117705.1_Zm-Mo17-REFERENCE-CAU-T2T-assembly_genomic.fna Zm-Mo17-REFERENCE-CAU-2.0.fa

wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/644/905/GCA_001644905.2_Zm-W22-REFERENCE-NRGENE-2.0/GCA_001644905.2_Zm-W22-REFERENCE-NRGENE-2.0_genomic.fna.gz

gunzip GCA_001644905.2_Zm-W22-REFERENCE-NRGENE-2.0_genomic.fna.gz 

mv GCA_001644905.2_Zm-W22-REFERENCE-NRGENE-2.0_genomic.fna Zm-W22-REFERENCE-NRGENE-2.0.fa
