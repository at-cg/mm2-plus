# run mm2-plus
../mm2plus_aoc1bs -t48 --cs -cx asm5 GCF_009914755.1_T2T-CHM13v2.0_genomic.fna GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o mm2plus.paf

# run minimap2
../mm2plus_base/minimap2 -t48 --cs -cx asm5 GCF_009914755.1_T2T-CHM13v2.0_genomic.fna GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o minimap2.paf
