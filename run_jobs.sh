#!/bin/bash 


in_dir='output/hrc_sample'
out_dir='output/hrc_es_jsons'
slurm_dir='slurm_jsons'

#local testing
#in_dir='./../annoq-data/hrc-test'
#out_dir='./../annoq-data/tmp11_'
#slurm_dir='./../annoq-data/slurm2'

mkdir -p $slurm_dir
mkdir -p $out_dir

for fp in `ls $in_dir` ; do
    echo $in_dir/$fp
    mkdir -p $out_dir/${fp}
    IN_FILE=$in_dir/${fp} OUT_DIR=$out_dir/${fp} \
    envsubst '$IN_FILE, $OUT_DIR' < hrc_batch.template > $slurm_dir/slurm_${fp}.slurm
    sbatch $slurm_dir/slurm_${fp}.slurm
done

