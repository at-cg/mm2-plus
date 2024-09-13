# build minimap2 without avx
cd minimap2_base && make clean && make profile=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_no_avx_base.paf 2> maize_mapped/no_avx_base.txt

# build minimap2 with avx
cd minimap2_base && make clean && make profile=1 avx=1 && cd ..
minimap2_base/minimap2 -t48 -cx asm5 maize/Zm-Mo17-REFERENCE-CAU-2.0.fa maize/Zm-W22-REFERENCE-NRGENE-2.0.fa -o maize_mapped/maize_PAT_avx_base.paf 2> maize_mapped/avx_base.txt