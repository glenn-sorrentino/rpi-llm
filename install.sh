#!/bin/bash

# Update and upgrade the system
sudo apt-get update && sudo apt-get upgrade -y

# Install required dependencies
sudo apt-get install -y python3 python3-pip python3-venv

# Create a Python virtual environment
python3 -m venv llm_env
source llm_env/bin/activate

# Create the project directory structure
mkdir -p llm_raspberry_pi
cd llm_raspberry_pi
mkdir datasets

# Install TensorFlow (or PyTorch) and Hugging Face Transformers library
pip install --upgrade pip
pip install -r requirements.txt

# Run the dataset downloading and pre-processing script
python download_datasets.py

# Launch the application
python app.py

