# build minimap2-hap with avx + par_chain
./minimap2_aoc2 -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_avx_chain_hap_2.paf 2> maize_mapped/avx_chain_hap_2.txt

# build minimap2 with avx + chain + btk
./minimap2_aoc2b -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_avx_chain_btk_hap_2.paf 2> maize_mapped/avx_chain_btk_hap_2.txt

# build minimap2 with avx + chain + btk + sort
./minimap2_aoc2bs -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_avx_chain_btk_sort_hap_2.paf 2> maize_mapped/avx_chain_btk_sort_hap_2.txt
