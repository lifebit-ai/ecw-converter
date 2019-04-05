# ecw-converter

Dockerised python scripts & Nextflow pipeline for converting ecw files to either geotiffs or Cloud Optimised Geotiffs (COGs).

## Motivation

The scripts have been used for converting a stream ecw file images from [Denmark aerial imagery source site](https://download.kortforsyningen.dk/content/geodanmark-ortofoto-blokinddelt) into coggs (which is a very high compute process).

Converting to full COGs is far better than creating regular GeoTiffs. The key benefit of a COG is that it is possible to get only a section of the image if required, rather than downloading the entire file. When working with large files and doing analysis on/viewing a specific section of the image, this becomes incredibly beneficial.
(There are also further differences)


## Quick run
The tool(s) can be run on:
* [command line with Docker](#running-on-the-command-line-with-docker)
* [command line with Nextflow](#running-on-the-command-line-with-nextflow)
* [Deploit with Docker](#running-docker-on-deploit)
* [Deploit with Nextflow](#running-nextflow-on-deploit)

If analysing lots of data it is recommended to use Nextflow rather than Docker alone for increased parallelisation. 

## Testdata
Bucket containing the images (300 zips of the .ecw format files) can be found at: [s3://lifebit-public](https://s3-eu-west-1.amazonaws.com/lifebit-public/)

![aws_data](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/aws_data.png)


## Docker
The docker image is [lifebitai/ecw_converter:latest](https://hub.docker.com/r/lifebitai/ecw_converter)
   
The docker image contains the scripts which were originally downloaded from [joe.peskett/ecw_converter](https://gitlab.officialstatistics.org/joe.peskett/ecw_converter.git) & were modified. 

The modifications included:
- changing the regex for input ECW files
- removing the pushing to S3 bucket
- adding python shebang lines

Dependencies for the scripts such as GDAL with .ecw drivers & Python are also installed in the image.

The docker image includes the following scripts:
- [`ecw_to_cog.sh`](ecw_converter/ecw_to_cog.sh) bash wrapper script to unzip files the input files and then run the scripts below
- [`ecw_convert_2_cog.py`](ecw_converter/ecw_convert_2_cog.py) scripts for converting .ecw files to both COGs and GeoTiffs. There are two gdal_translate processes. Without the second process, you will NOT create a valid COG
- [`validate_cog.py`](ecw_converter/validate_cog.py) validate whether a COG is a valid, fully compliant COG

### (Re)building the Docker image

If you wish to make any modifications to the docker image you can do so with the steps below:
```bash
git clone https://github.com/lifebit-ai/ecw-converter.git && cd ecw-converter
docker build -t <DockerHubUsername>/ecw_converter:<tag> .
# you can then use `docker login` & `docker push <DockerHubUsername>/ecw_converter:<tag>` to push to DockerHub
```

### Running on the command line with Docker

If you have docker installed, and zipped ECW files in you current directory the tool can be run with the following command:
```bash
# you can download a zipped ecw file with `wget https://s3-eu-west-1.amazonaws.com/lifebit-public/10km_2017_612_62_ECW_UTM32-ETRS89.zip`
docker run -v $PWD:$PWD -w $PWD lifebitai/ecw_converter ecw_to_cog.sh
```

## Deploit

Deploit is a bioinformatics platform, developed by Lifebit, where you can run your analysis over the Cloud/AWS.

You can create an account/log in [here](https://deploit.lifebit.ai/login)

![deploit](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/deploit.png)

### Running Docker on Deploit

#### Import the Docker image from DockerHub:

Navigate to the pipelines page, click new to import a new pipeline. Then select Docker & paste the URL from DockerHub eg: https://hub.docker.com/r/lifebitai/ecw_converter

![import](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/import_docker.png)


#### Running a job

You can then click the pipeline under the "My pipelines" section and select data/input parameters:

![run_job](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/run_job.png)

No input parameters are required. Currently, all of the input zipped ecw files are set using the working directory. All of the files in the working directory will then be unzipped and the ecw files converted.

#### Setting resources

Select a project & instance:

![instance](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/instance.png)

## Nextflow

### Running on the command line with Nextflow

If you have Nextflow & Docker installed, and zipped ECW files in one of your directories the pipeline can be run with the following command:
```bash
# you can download a zipped ecw file with `wget https://s3-eu-west-1.amazonaws.com/lifebit-public/10km_2017_612_62_ECW_UTM32-ETRS89.zip`
nextflow run main.nf --input_folder <your_folder>
```

### Running Nextflow on Deploit

#### Import the Nextflow pipeline from GitHib:

Navigate to the pipelines page, click new to import a new pipeline. Then select Nextflow & paste the URL from GitHub eg: https://github.com/lifebit-ai/ecw-converter

![import_nextflow](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/import_nextflow.png)


#### Running a Nextflow job

You can then click the pipeline under the "My pipelines" section and select data/input parameters:

The `--input_folder` is a required parameter. It must contain all of the input zipped ecw files to be unzipped and the ecw files converted. The data can be set by clicking the blue arrow and selecting your data either from an S3 bucket or by uploading the data. 


![run_nextflow_job](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/run_nextflow_job.png)

#### Setting resources

Select a project & instance:

![instance_nextflow](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/instance_nextflow.png)

## Outputs

From running the `ecw_to_cog.sh` script the following folders/files are generated:
* `zip` the input .zip files are moved to this directory
* `tif` directory to store the generated .tif files
* `logs`
    * `validate_cog.log` stdout from `validate_cog.py`
    * `unzip.log` stdout from unzipping of the files
    * `ecw_convert_2_cog.log` stdout from `ecw_convert_2_cog.py`
* `img`
    * `compliant-cog` directory to contain COG files
* `ecw` directory to store the .ecw files once unzipped
