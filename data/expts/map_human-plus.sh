# run mm2-plus with avx + olp
./minimap2_ao -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_avx_chain_plus_olp.paf 2> human_mapped/avx_chain_plus_olp.txt

# run mm2-plus with avx + olp + par_chain
./minimap2_aoc1 -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_avx_chain_plus.paf 2> human_mapped/avx_chain_plus.txt

# run mm2-plus with avx + olp + par_chain + btk
./minimap2_aoc1b -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_avx_chain_btk_plus.paf 2> human_mapped/avx_chain_btk_plus.txt

# run mm2-plus with avx + olp + par_chain + btk + sort
./minimap2_aoc1bs -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_avx_chain_btk_sort_plus.paf 2> human_mapped/avx_chain_btk_sort_plus.txt
