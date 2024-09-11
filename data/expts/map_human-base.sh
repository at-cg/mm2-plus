# run minimap2 without avx
minimap2_base/minimap2 -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_no_avx_base.paf 2> human_mapped/no_avx_base.txt

# build minimap2 with avx
cd minimap2_base && make clean && make profile=1 avx=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm5 human/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  human/GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o human_mapped/CHM13_HG002_PAT_avx_base.paf 2> human_mapped/avx_base.txt
