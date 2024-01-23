# AnnoQ Database Tools

Tools for processing and loading data into Elasticsearch and mapping for AnnoQ

## Installation

Clone the repository and set up the required environment:

```bash
git clone [repository-url]
cd [repository-name]
```

install packages in requirement.txt

## 1.1  Conversion Tool

This tool is designed for converting VCF files (in TSV format) with added PANTHER and ENHANCER functions into JSON format for efficient processing with Elasticsearch. It includes functionalities to process data in bulk, generate JSON files, and handle them in both local and HPC cluster environments.

- Converts VCF files to JSON.
- Adds unique IDs to each record (combining chromosome, position, reference, and alternate values).
- Supports execution in both local and cluster environments.

## Prerequisites

- Python 3.9.12 or higher.
- Elasticsearch tested with 8.5.*.
- HPC

## Setup commands for environment (if applicable)

### Usage

#### Local Execution

To run the script locally, use the following command:

```bash
bash scripts/run_jobs.sh --work_name [work_name] --base_dir [base_directory] --es_index [es_index] --local
```

#### Cluster Execution

For execution on a cluster with Slurm Workload Manager, use:

```bash
bash scripts/run_jobs.sh --work_name [work_name] --base_dir [base_directory] --es_index [es_index]
```

Replace [work_name], [base_directory], and [es_index] with your specific parameters.

#### Parameters

--work_name - Name of the work or task.
--base_dir - Base directory for input and output data.
--es_index - Elasticsearch index name.
--local - (Optional) Flag to run the script locally.


## Script Details

The main script run_jobs.sh handles the overall process flow:

1. Validates input parameters and directories.
2. Prepares and cleans output and slurm directories.
3. Iterates over files in the input directory for processing.
4. Generates and executes Slurm batch scripts for each file or runs them locally.

The batch template (db_batch.template) includes:

SLURM job configurations.
Environment setup.
Execution of the Python script for JSON conversion.




## Dependents on two data files

* ./data/doc_type.pkl
* ./data/annoq_mapping.json

## Converting and Indexing Elasticsearch

### Converting

1. install packages in requirements.txt
2. convert the resulting wgsa_add PANTHER and ENHANCER vcf or tsc files to json
3. use run_jobs.sh for production and run_job local for local setup

### Indexing 
1. run `sh scripts-test-server/create_index.sh` to create index.
2. run `python3 create_mapping.py` to load mapping
3. run `python index_es_json.py` to load into elasticsearch
