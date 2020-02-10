# SbmlToSbol

To run, use Docker.

1. From the console, type `bash docker_build.sh` to build the Docker image.
2. To run, type `bash docker_run.sh`. The file `docker_run.sh` contains the command line arguments as follows:
    * `True` Boolean flag, specifying whether an RBS site should be added to each gene.
    * `/out/sbol.xml` The output file.
    * `/data` The directory containing in input files (in SBML format - essentially the output from Selenzyme).