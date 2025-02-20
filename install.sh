#!/bin/bash

# ocr
# Name of the conda environment
ENV_NAME=EasyOCR

# Path to the conda executable
CONDA_PATH=$(which conda)

# Check if conda is installed
if [ -z "$CONDA_PATH" ]; then
    echo "Conda could not be found. Please install conda first."
    exit
fi

# Initialize conda
eval "$($CONDA_PATH shell.bash hook)"

# Create the conda environment
echo "Creating conda environment..."
conda create -n $ENV_NAME python=3.11 -y

# Activate the conda environment
echo "Activating conda environment..."
conda activate $ENV_NAME

cd $ENV_NAME

# Install the requirements from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt file not found. Please provide the file."
    exit
fi

echo "Conda environment '$ENV_NAME' is ready."

echo "Deactivating conda environment..."
conda deactivate
cd ..

# llm
# Name of the conda environment
ENV_NAME=QWEN

# Create the conda environment
echo "Creating conda environment..."
conda create -n $ENV_NAME python=3.11 -y

# Activate the conda environment
echo "Activating conda environment..."
conda activate $ENV_NAME

cd $ENV_NAME

# Install the requirements from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt file not found. Please provide the file."
    exit
fi

echo "Conda environment '$ENV_NAME' is ready."

echo "Deactivating conda environment..."
conda deactivate
cd ..

# sdxl
# Name of the conda environment
ENV_NAME=SDXL

# Create the conda environment
echo "Creating conda environment..."
conda create -n $ENV_NAME python=3.11 -y

# Activate the conda environment
echo "Activating conda environment..."
conda activate $ENV_NAME

cd $ENV_NAME

# Install the requirements from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt file not found. Please provide the file."
    exit
fi

echo "Conda environment '$ENV_NAME' is ready."

echo "Deactivating conda environment..."
conda deactivate
cd ..

# central api
# Name of the conda environment
ENV_NAME=BookReader

# Create the conda environment
echo "Creating conda environment..."
conda create -n $ENV_NAME python=3.9 -y

# Activate the conda environment
echo "Activating conda environment..."
conda activate $ENV_NAME

cd $ENV_NAME

# Install the requirements from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt file not found. Please provide the file."
    exit
fi

echo "Conda environment '$ENV_NAME' is ready."

echo "Deactivating conda environment..."
conda deactivate
cd ..

echo "Installation complete."