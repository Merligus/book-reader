#!/bin/bash

# Path to the conda executable
CONDA_PATH=$(which conda)

# Check if conda is installed
if [ -z "$CONDA_PATH" ]; then
    echo "Conda could not be found. Please install conda first."
    exit
fi

# Initialize conda
eval "$($CONDA_PATH shell.bash hook)"

# ocr
conda activate EasyOCR
gunicorn -w 1 -b 0.0.0.0:7861 EasyOCR:app --env flask_key="flask_key_ocr" &
conda deactivate

# llm
conda activate QWEN
gunicorn -w 1 -b 0.0.0.0:7862 QWEN:app --env flask_key="flask_key_qwen" &
conda deactivate

# sdxl
conda activate SDXL
gunicorn -w 1 -b 0.0.0.0:7863 SDXL:app --env flask_key="flask_key_sdxl" &
conda deactivate

# book reader
conda activate BookReader
gunicorn -w 1 -b 0.0.0.0:7860 BookReader:app --env flask_key="flask_key_book_reader_orchestrator" &
conda deactivate

wait

echo "Completed."