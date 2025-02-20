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

# List of conda environments to activate
ENVIRONMENTS=("EasyOCR:7861" "QWEN:7862" "SDXL:7863" "BookReader:7860")

# Start multiple Gunicorn processes in the background and capture their PIDs in a list
GUNICORN_PIDs=()

# Loop through each environment and activate it
for ENV_NAME_VERSION in "${ENVIRONMENTS[@]}"; do
    # get environment name and python version
    IFS=':' read -r ENV_NAME PORT <<< "$ENV_NAME_VERSION"

    conda activate $ENV_NAME
    gunicorn -w 1 -b 0.0.0.0:$PORT $ENV_NAME:app --env flask_key="flask_key_$ENV_NAME" & GUNICORN_PIDs+=($!)
    conda deactivate
done

conda activate BookReader
python BookReader/app.py
conda deactivate

# Function to kill Gunicorn processes on script exit
function cleanup {
    echo "Shutting down Gunicorn processes..."
    for PID in "${GUNICORN_PIDs[@]}"; do
        kill -9 $PID
    done
    exit
}

# Trap Ctrl+C (SIGINT) and call the cleanup function
trap cleanup SIGINT

# Wait for Gunicorn processes to finish (this keeps the script running)
for PID in "${GUNICORN_PIDs[@]}"; do
    wait $PID
done

echo "Completed."