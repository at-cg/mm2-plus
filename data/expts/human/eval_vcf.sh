#!/usr/bin/bash
# Compute VCF files
ref_fasta=GCF_009914755.1_T2T-CHM13v2.0_genomic.fna
samtools faidx ${ref_fasta}
cat minimap2.paf | sort -k6,6 -k8,8n | paftools.js call -f "$ref_fasta" - | bgzip > minimap2.vcf.gz
cat mm2plus.paf | sort -k6,6 -k8,8n | paftools.js call  -f "$ref_fasta" - | bgzip > mm2plus.vcf.gz

# index VCF files
bcftools index --csi minimap2.vcf.gz
bcftools index --csi mm2plus.vcf.gz

# Compare the VCF files
bcftools isec -p out_dir -Oz minimap2.vcf.gz mm2plus.vcf.gz

# index files
bcftools index --csi out_dir/0000.vcf.gz
bcftools index --csi out_dir/0001.vcf.gz
bcftools index --csi out_dir/0002.vcf.gz

# Generate statistics
bcftools stats out_dir/0000.vcf.gz > out_dir/fp_stats.txt
bcftools stats out_dir/0001.vcf.gz > out_dir/fn_stats.txt
bcftools stats out_dir/0002.vcf.gz > out_dir/tp_stats.txt

python3 get_f1.py

