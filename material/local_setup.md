# Local setup

## Setup Python

There are many possible ways. Here I highlight using miniforge3.

### Download Mini-Forge distribution

> https://conda-forge.org/download/


For a VM running Ubuntu 22.04, select the Linux x86_64 installer.

```bash
# follow the installation instructions on the website, or run the following command to download and install Miniforge3:
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh | bash
```

> close the terminal and open a new one to activate the conda environment after installation.

### Create a conda environment

```bash
conda create -n pyopenms python=3.14
conda activate pyopenms
pip install pyopenms    
```

## Install docker

Follow the instructions on the Docker website to install Docker on your system, e.g. 
for Ubuntu 22.04, you can follow the instructions here:
https://docs.docker.com/engine/install/ubuntu/


And if you see errors also add your user to the docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Install nextflow

As you already have conda installed, you can install nextflow using conda:

```bash
conda activate pyopenms
conda install -c bioconda nextflow
```

## ThermoRawFileParser

- conversion to mzML from Thermo RAW files.

```bash
wget https://github.com/CompOmics/ThermoRawFileParser/releases/download/v.2.0.0-dev/ThermoRawFileParser-v.2.0.0-dev-linux.zip
unzip ThermoRawFileParser-v.2.0.0-dev-linux.zip -d ThermoRawFileParser
echo "alias trfp='$(pwd)/ThermoRawFileParser/ThermoRawFileParser'" >> ~/.bashrc
``` 
