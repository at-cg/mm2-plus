 build minimap2-hap with profile
cd minimap2_base && make clean && make profile=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/no_avx_base.paf 2> barley_mapped/no_avx_base.txt

# build minimap2-hap with avx + profile
cd minimap2_base && make clean && make profile=1 avx=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/avx_base.paf 2> barley_mapped/avx_base.txt

# build minimap2 with avx + chain + btk + sort (Inter-chromosomal chaining)
./minimap2_aoc1bs -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_btk_sort_hap_1.paf 2> barley_mapped/avx_chain_btk_sort_hap_1.txt

# build minimap2 with avx + chain + btk + sort (Intra-chromosomal chaining)
./minimap2_aoc2bs -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_btk_sort_hap_2.paf 2> barley_mapped/avx_chain_btk_sort_hap_2.txt
