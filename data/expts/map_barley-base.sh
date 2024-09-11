# build minimap2-hap with profile
cd minimap2_base && make clean && make profile=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/no_avx_base.paf 2> barley_mapped/no_avx_base.txt

# build minimap2-hap with avx + profile
cd minimap2_base && make clean && make profile=1 avx=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm5 barley/Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa barley/GCA_902500625.1_GPv1_genomic.fna -o barley_mapped/avx_base.paf 2> barley_mapped/avx_base.txt
