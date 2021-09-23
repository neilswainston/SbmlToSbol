# SbmlToSbol

## Install
### Install requirements
#### From PIP
From the console, type:
```
pip install --upgrade pip
pip install -r requirements.txt
```
#### From Conda
From the console, type:
```
conda update --all -y
conda env create -f environment.yml
```

## Run
If dependencies have been installed within a conda environment, run:
```
conda activate sbml2sbol
```
or directly
```
conda run --name sbml2sbol <command>
```
where command is the one below.

Then, run in a terminal:
```
python -m sbml2sbol --input tests/data --outfile result.sbol
```

## Docker

1. From the console, type `bash docker/build.sh` to build the Docker image.
2. To run, type `bash docker/run.sh`. The file `docker/run.sh` expect the following command line arguments:
    * `input_folder` The directory (with absolute path) containing in input files (in SBML format - essentially the output from Selenzyme).
    * `outfile` The output filename (with absolute path).
    * `RBS` (optional) Boolean flag, specifying whether an RBS site should be added to each gene (default: True).


## Test
After installing `pytest`, run:
```
export PYTHONPATH=$PWD
pytest -v tests
```