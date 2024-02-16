# AnnoQ Database Processing Suite

## Overview

The Annoq Data Processing Suite is designed for efficient conversion and handling of AnnoQ PANTHER and ENHANCER function data files for use with Elasticsearch. It consists of a Bash script for managing the overall data processing workflow and a Python script for converting tab-separated values (TSV) files into a JSON format optimized for Elasticsearch.

## Installation

Clone the repository and set up the required environment:

```bash
git clone [repository-url]
cd [repository-name]
```

install packages in requirement.txt

## Prerequisites

- Python 3.9.12 or higher.
- Elasticsearch tested with 8.5.*.
- HPC
  
## 1.1  Conversion Tool

This tool is designed for converting VCF files (in TSV format) with added PANTHER and ENHANCER functions into JSON format for efficient processing with Elasticsearch. It includes functionalities to process data in bulk, generate JSON files, and handle them in both local and HPC cluster environments.

- Converts VCF files to JSON.
- Adds unique IDs to each record (combining chromosome, position, reference, and alternate values).
- Supports execution in both local and cluster environments.


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

## 1.2 Loading/Indexing Tool

This tool show instructions how to use a set of bash and Python scripts designed for indexing documents into Elasticsearch. These tools allow you to create or recreate an Elasticsearch index with specific mappings and settings, and then bulk load JSON documents into the index from a specified directory.

### Dependents on two data files

* ./data/doc_type.pkl
* ./data/annoq_mapping.json

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Elasticsearch
- Python 3.10
- Ensure your Elasticsearch instance is running and accessible.

### Usage

Bash Script: run_es_job.sh
The bash script serves as the entry point for the indexing process. It validates the input arguments, initializes the Elasticsearch index with specified mappings and settings, and then proceeds to index documents from a given input directory.

```bash
bash run_es_job.sh --index_name <index_name> --mappings_file <mappings_file> --settings_file <settings_file> --input_dir <input_dir>
```

#### Arguments

- --index_name: The name of the Elasticsearch index.
- --mappings_file: Path to the JSON file containing index mappings.
- --settings_file: Path to the JSON file containing index settings.
- --input_dir: Directory containing JSON documents to be indexed.

### Python Script: reinit

The reinit Python module is responsible for creating or recreating the Elasticsearch index based on the provided mappings and settings.

### Usage Example

```bash
python -m src.reinit --index_name "your_index_name" --mappings_file "path/to/mappings.json" --settings_file "path/to/settings.json"
```

### Python Script: index_es_json

The index_es_json Python module indexes JSON documents into the specified Elasticsearch index. It supports bulk loading through different strategies, including parallel, streaming, and standard bulk load.

#### Usage Example

```bash
python3 -m src.index_es_json "/path/to/input_directory"
```

## Detailed Steps

Prepare Index Mappings and Settings: Create JSON files containing your index mappings and settings.
Index Initialization: Use the reinit script to create or recreate the index with the specified mappings and settings.
Document Indexing: Use the index_es_json script to bulk load documents into the index from the specified directory.

Logging
The index_es_json script logs its progress and any errors encountered during the indexing process. Check the logfile.log for details.

## Troubleshooting

Make sure to run run_job.sh first
Ensure Elasticsearch is running and accessible.
Validate the JSON format of your mappings and settings files.
Check the logfile.log for any errors or warnings that occurred during indexing.
