# run mm2-plus with avx + par_olp
./minimap2_ao -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_avx_chain_plus_olp.paf 2> maize_mapped/avx_chain_plus_olp.txt

# run mm2-plus with avx + par_chain
./minimap2_aoc1 -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_avx_chain_plus.paf 2> maize_mapped/avx_chain_plus.txt

# run mm2-plus with avx + chain + btk
./minimap2_aoc1b -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_avx_chain_btk_plus.paf 2> maize_mapped/avx_chain_btk_plus.txt

# run mm2-plus with avx + chain + btk + sort
./minimap2_aoc1bs -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_avx_chain_btk_sort_plus.paf 2> maize_mapped/avx_chain_btk_sort_plus.txt
