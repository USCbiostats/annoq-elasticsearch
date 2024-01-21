#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 --work_name <work_name> --base_dir <base_dir> --es_index <es_index> [--local]"
    exit 1
}

# Parse named arguments
LOCAL_EXECUTION=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --work_name) WORK_NAME="$2"; shift ;;
        --base_dir) BASE_DIR="$2"; shift ;;
        --es_index) ES_INDEX="$2"; shift ;;
        --local) LOCAL_EXECUTION=true ;;
        *) echo "Unknown parameter: $1"; usage ;;
    esac
    shift
done

# Check if all required parameters are set
if [ -z "$WORK_NAME" ] || [ -z "$BASE_DIR" ] || [ -z "$ES_INDEX" ]; then
    echo "Error: All required arguments are not provided."
    usage
fi

# Check if base directory exists
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Base directory does not exist."
    exit 1
fi

echo "Running work name: $WORK_NAME using base dir: $BASE_DIR"

IN_DIR=$BASE_DIR/annoq-data-builder/wgsa_add/output/$WORK_NAME
OUT_DIR=$BASE_DIR/annoq-database/output/$WORK_NAME
SLURM_DIR=$BASE_DIR/annoq-database/slurm/$WORK_NAME
SBATCH_TEMPLATE=$BASE_DIR/annoq-database/src/db_batch.template

# Check if input directory exists
if [ ! -d "$IN_DIR" ]; then
    echo "Error: Input directory does not exist."
    exit 1
fi

# Check if output and slurm directories exist and ask for confirmation before removing them
if [ -d "$OUT_DIR" ] || [ -d "$SLURM_DIR" ]; then
    echo "About to remove the following directories:"
    [ -d "$OUT_DIR" ] && echo "Output Directory: $OUT_DIR"
    [ -d "$SLURM_DIR" ] && echo "Slurm Directory: $SLURM_DIR"
    read -p "Are you sure you want to proceed? (yes/no) " CONFIRMATION
    if [ "$CONFIRMATION" != "yes" ]; then
        echo "Operation cancelled by the user."
        exit 1
    fi

    # Cleanup the output and slurm directories
    rm -rf $OUT_DIR $SLURM_DIR
fi

# Create output and slurm directories
mkdir -p $SLURM_DIR $OUT_DIR

# Iterate over files in input directory
for FP in $(ls $IN_DIR) ; do
    echo "Processing file: $IN_DIR/$FP"
    mkdir -p $OUT_DIR/${FP}
    BASE_DIR=$BASE_DIR IN_FILE=$IN_DIR/${FP} OUT_DIR=$OUT_DIR/${FP} ES_INDEX=$ES_INDEX \
    envsubst '$BASE_DIR, $IN_FILE, $OUT_DIR, $ES_INDEX' < $SBATCH_TEMPLATE > $SLURM_DIR/slurm_${FP}.slurm
    
    # Check if local execution is requested
    if [ "$LOCAL_EXECUTION" = true ]; then
        bash $SLURM_DIR/slurm_${FP}.slurm
    else
        sbatch $SLURM_DIR/slurm_${FP}.slurm
    fi
done

# local execution example:
# bash scripts/run_jobs.sh --work_name test_vcfs --base_dir .. --es_index annoq-annotations-v2

# cluster execution example:
# bash scripts/run_jobs.sh --work_name HRC_03_07_19 --base_dir /scratch2/xxx --es_index annoq-annotations-v2
