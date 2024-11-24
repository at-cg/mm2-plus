# run mm2-plus with avx + olp
./mm2plus_ao -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  primates/GCF_029289425.2_NHGRI_mPanPan1-v2.0_pri_genomic.fna -o primates_mapped/CHM13_PanPan_PAT_avx_chain_plus_olp.paf 2> primates_mapped/avx_chain_plus_olp.txt

# run mm2-plus with avx + par_chain
./mm2plus_aoc1 -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  primates/GCF_029289425.2_NHGRI_mPanPan1-v2.0_pri_genomic.fna -o primates_mapped/CHM13_PanPan_PAT_avx_chain_plus.paf 2> primates_mapped/avx_chain_plus.txt

# run mm2-plus with avx + chain + btk
./mm2plus_aoc1b -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  primates/GCF_029289425.2_NHGRI_mPanPan1-v2.0_pri_genomic.fna -o primates_mapped/CHM13_PanPan_PAT_avx_chain_btk_plus.paf 2> primates_mapped/avx_chain_btk_plus.txt

# run mm2-plus with avx + chain + btk + sort
./mm2plus_aoc1bs -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna primates/GCF_029289425.2_NHGRI_mPanPan1-v2.0_pri_genomic.fna -o primates_mapped/CHM13_PanPan_PAT_avx_chain_btk_sort_plus.paf 2> primates_mapped/avx_chain_btk_sort_plus.txt
