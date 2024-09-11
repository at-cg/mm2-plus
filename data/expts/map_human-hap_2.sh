# build minimap2-hap with avx + par_chain
./minimap2_aoc2 -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_avx_chain_hap_2.paf 2> human_mapped/avx_chain_hap_2.txt

# build minimap2 with avx + chain + btk
./minimap2_aoc2b -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_avx_chain_btk_hap_2.paf 2> human_mapped/avx_chain_btk_hap_2.txt

# build minimap2 with avx + chain + btk + sort
./minimap2_aoc2bs -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_avx_chain_btk_sort_hap_2.paf 2> human_mapped/avx_chain_btk_sort_hap_2.txt
