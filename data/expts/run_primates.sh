# build minimap2 without avx
cd minimap2_base && make clean && make profile=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna  primates/mPanPan1.pat.cur.20231122.fasta -o primates_mapped/CHM13_PanPan_PAT_no_avx_base.paf 2> primates_mapped/no_avx_base.txt

# build minimap2 with avx
cd minimap2_base && make clean && make profile=1 avx=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna primates/mPanPan1.pat.cur.20231122.fasta -o primates_mapped/CHM13_PanPan_PAT_avx_base.paf 2> primates_mapped/avx_base.txt

# build minimap2 with avx + chain + btk + sort
./minimap2_aoc1bs -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna primates/mPanPan1.pat.cur.20231122.fasta -o primates_mapped/CHM13_PanPan_PAT_avx_chain_btk_sort_hap_1.paf 2> primates_mapped/avx_chain_btk_sort_hap_1.txt

# build minimap2 with avx + chain + btk + sort
./minimap2_aoc2bs -t48 -cx asm20 primates/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna primates/mPanPan1.pat.cur.20231122.fasta -o primates_mapped/CHM13_PanPan_PAT_avx_chain_btk_sort_hap_2.paf 2> primates_mapped/avx_chain_btk_sort_hap_2.txt
