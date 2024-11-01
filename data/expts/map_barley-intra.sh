# build minimap2-hap with avx + par_chain
./minimap2_aoc2 -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_hap_2.paf 2> barley_mapped/avx_chain_hap_2.txt

# build minimap2 with avx + chain + btk
./minimap2_aoc2b -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_btk_hap_2.paf 2> barley_mapped/avx_chain_btk_hap_2.txt

# build minimap2 with avx + chain + btk + sort
./minimap2_aoc2bs -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_btk_sort_hap_2.paf 2> barley_mapped/avx_chain_btk_sort_hap_2.txt
