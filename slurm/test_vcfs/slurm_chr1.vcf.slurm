#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=50:00:00
#SBATCH --account=pdthomas_136
#SBATCH --partition=thomas
#SBATCH --mem-per-cpu=20G
#SBATCH --mail-type=end,fail
#SBATCH --mail-user=mushayah@usc.edu

# Define directories and files
BASE_DIR=".."
IN_FILE="../annoq-data-builder/wgsa_add/output/test_vcfs/chr1.vcf"
OUT_DIR="../annoq-database/output/test_vcfs/chr1.vcf"
ES_INDEX="annoq-annotations-v2"
DOC_TYPE_FILE="../annoq-database/data/doc_type.pkl"

# Check if the input file and document type file exist
if [ ! -f "../annoq-data-builder/wgsa_add/output/test_vcfs/chr1.vcf" ]; then
    echo "Error: Input file does not exist - ../annoq-data-builder/wgsa_add/output/test_vcfs/chr1.vcf"
    exit 1
fi

if [ ! -f "$DOC_TYPE_FILE" ]; then
    echo "Error: Document type file does not exist - $DOC_TYPE_FILE"
    exit 1
fi

# Check if output directory exists, create if not
if [ ! -d "../annoq-database/output/test_vcfs/chr1.vcf" ]; then
    echo "Output directory does not exist, creating now: ../annoq-database/output/test_vcfs/chr1.vcf"
    mkdir -p "../annoq-database/output/test_vcfs/chr1.vcf"
fi

# Load the required module and activate virtual environment
module load python/3.9.12
python3 --version
source venv/bin/activate

# Run the Python script
echo "Starting JSON conversion: ../annoq-data-builder/wgsa_add/output/test_vcfs/chr1.vcf -> ../annoq-database/output/test_vcfs/chr1.vcf"
echo "Start time: $(date)"
python3 -m src.convert_to_json -i "../annoq-data-builder/wgsa_add/output/test_vcfs/chr1.vcf" -o "../annoq-database/output/test_vcfs/chr1.vcf" --es_index "annoq-annotations-v2" --doc_type_file "$DOC_TYPE_FILE"
echo "End time: $(date)"
