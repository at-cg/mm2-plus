# run mm2-plus with avx + par_olp
./mm2plus_ao -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_plus_olp.paf 2> barley_mapped/avx_chain_plus_olp.txt

# run mm2-plus with avx + par_chain
./mm2plus_aoc1 -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_plus.paf 2> barley_mapped/avx_chain_plus.txt

# run mm2-plus with avx + chain + btk
./mm2plus_aoc1b -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_btk_plus.paf 2> barley_mapped/avx_chain_btk_plus.txt

# run mm2-plus with avx + chain + btk + sort
./mm2plus_aoc1bs -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/barley_avx_chain_btk_sort_plus.paf 2> barley_mapped/avx_chain_btk_sort_plus.txt
