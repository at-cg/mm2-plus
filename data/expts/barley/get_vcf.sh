# mm2-plus
../mm2plus_aoc1bs -t48 -x asm5 Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa GCA_902500625.1_GPv1_genomic.fna -o mm2plus.paf

# minimap2
../mm2plus_base/minimap2 -t48 --cs -cx asm5 --cs Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa GCA_902500625.1_GPv1_genomic.fna -o minimap2.paf
