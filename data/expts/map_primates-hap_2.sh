# build minimap2-hap with avx + par_chain
./minimap2_aoc2 -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  primates/mPanPan1.pat.cur.20231122.fasta -o primates_mapped/CHM13_PanPan_PAT_avx_chain_hap_2.paf 2> primates_mapped/avx_chain_hap_2.txt

# build minimap2 with avx + chain + btk
./minimap2_aoc2b -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  primates/mPanPan1.pat.cur.20231122.fasta -o primates_mapped/CHM13_PanPan_PAT_avx_chain_btk_hap_2.paf 2> primates_mapped/avx_chain_btk_hap_2.txt

# build minimap2 with avx + chain + btk + sort
./minimap2_aoc2bs -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna primates/mPanPan1.pat.cur.20231122.fasta -o primates_mapped/CHM13_PanPan_PAT_avx_chain_btk_sort_hap_2.paf 2> primates_mapped/avx_chain_btk_sort_hap_2.txt
