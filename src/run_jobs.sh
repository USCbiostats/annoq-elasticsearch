#!/bin/bash 

if [ "$#" -ne 2 ]; then
  echo "Error: Exactly 2 arguments are required."
  echo "Usage: $0 <work_name> <wgsa_dir>"
  exit 1
fi

work_name=$1
base_dir=$2

echo "running work name: $work_name using base dir: $base_dir"

in_dir=$base_dir/annoq-data-builder/wgsa_add/output/$work_name
out_dir=$base_dir/annoq-database/output/$work_name
slurm_dir=$base_dir/annoq-database/slurm/$work_name
sbatch_template=$base_dir/annoq-database/src/db_batch.template

rm -rf $out_dir $slurm_dir

mkdir -p $slurm_dir
mkdir -p $out_dir

for fp in `ls $in_dir` ; do
    echo $in_dir/$fp
    mkdir -p $out_dir/${fp}
    BASE_DIR=$base_dir IN_FILE=$in_dir/${fp} OUT_DIR=$out_dir/${fp} \
    envsubst '$BASE_DIR, $IN_FILE, $OUT_DIR' < $sbatch_template > $slurm_dir/slurm_${fp}.slurm
    sbatch $slurm_dir/slurm_${fp}.slurm
done