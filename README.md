# ecw-converter

Dockerised python scripts & Nextflow pipeline for converting ecw files to either Geotiffs or Cloud Optimised Geotiffs (COGs).

- [Motivation](https://github.com/lifebit-ai/ecw-converter#motivation)
- [Quick Run](https://github.com/lifebit-ai/ecw-converter#quick-run)
- [Testdata](https://github.com/lifebit-ai/ecw-converter#testdata)
- [Docker](https://github.com/lifebit-ai/ecw-converter#docker)
    - [Rebuilding the docker image](https://github.com/lifebit-ai/ecw-converter#rebuilding-the-docker-image) 
    - [Running on the command line with Docker](https://github.com/lifebit-ai/ecw-converter#running-on-the-command-line-with-docker)
- [Deploit](https://github.com/lifebit-ai/ecw-converter#deploit)
    - [Running docker on Deploit](https://github.com/lifebit-ai/ecw-converter#running-docker-on-deploit) 
        - [Import the docker image from DockerHub](https://github.com/lifebit-ai/ecw-converter#import-the-docker-image-from-dockerhub)
        - [Running a job](https://github.com/lifebit-ai/ecw-converter#running-a-job)
        - [Setting resources](https://github.com/lifebit-ai/ecw-converter#setting-resources)
- [Nextflow](https://github.com/lifebit-ai/ecw-converter#nextflow)
    - [Running on the command line](https://github.com/lifebit-ai/ecw-converter#running-on-the-command-line-with-nextflow)
    - [Running Nextflow on Deploit](https://github.com/lifebit-ai/ecw-converter#running-nextflow-on-deploit)
        - [Import the Nextflow pipeline from GitHub](https://github.com/lifebit-ai/ecw-converter#import-the-nextflow-pipeline-from-githib)
        - [Running a Nextflow job](https://github.com/lifebit-ai/ecw-converter#running-a-nextflow-job)
        - [Setting resources](https://github.com/lifebit-ai/ecw-converter#setting-resources-1)
- [Cost estimate](https://github.com/lifebit-ai/ecw-converter#cost-estimate)
- [Outputs](https://github.com/lifebit-ai/ecw-converter#outputs)

## Motivation

The scripts have been used for converting a stream ecw file images from [Denmark aerial imagery source site](https://download.kortforsyningen.dk/content/geodanmark-ortofoto-blokinddelt) into COGs (which is a very high compute process).

Converting to full COGs is far better than creating regular Geotiffs. The key benefit of a COG is that it is possible to get only a section of the image if required, rather than downloading the entire file. When working with large files and doing analysis on/viewing a specific section of the image, this becomes incredibly beneficial.
(There are also further differences)


## Quick run
The tool(s) can be run on:
* [command line with Docker](#running-on-the-command-line-with-docker)
* [command line with Nextflow](#running-on-the-command-line-with-nextflow)
* [Deploit with Docker](#running-docker-on-deploit)
* [Deploit with Nextflow](#running-nextflow-on-deploit) (recommended)

If analysing lots of data it is recommended to use Nextflow rather than Docker alone for increased parallelisation. 

## Testdata
Bucket containing the images (300 zips of the .ecw format files) can be found at: [s3://lifebit-public](https://s3.console.aws.amazon.com/s3/buckets/lifebit-public/?region=eu-west-1&tab=overview#)

![aws_data](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/aws_data.png)


## Docker
The docker image is [lifebitai/ecw_converter:latest](https://hub.docker.com/r/lifebitai/ecw_converter)
   
The docker image contains the scripts which were originally downloaded from [joe.peskett/ecw_converter](https://gitlab.officialstatistics.org/joe.peskett/ecw_converter.git) & were modified. 

The modifications included:
- changing the regex for input ECW files
- removing the pushing to an S3 bucket as this is handled by Deploit
- adding python shebang lines

Dependencies for the scripts such as GDAL with .ecw drivers & Python are also installed in the image.

The docker image includes the following scripts:
- [`ecw_to_cog.sh`](ecw_converter/ecw_to_cog.sh) bash wrapper script to unzip files the input files and then run the scripts below
- [`ecw_convert_2_cog.py`](ecw_converter/ecw_convert_2_cog.py) scripts for converting .ecw files to both COGs and Geotiffs. There are two gdal_translate processes. Without the second process, you will NOT create a valid COG
- [`validate_cog.py`](ecw_converter/validate_cog.py) validate whether a COG is a valid, fully compliant COG

### (Re)building the Docker image

If you wish to make any modifications to the docker image you can do so with the steps below:
```bash
git clone https://github.com/lifebit-ai/ecw-converter.git && cd ecw-converter
docker build -t <DockerHubUsername>/ecw_converter:<tag> .
# you can then use `docker login` & `docker push <DockerHubUsername>/ecw_converter:<tag>` to push to DockerHub
```

Once the docker image has been built & pushed to the DockerHub registry. (Which has already been done under the lifebitai DockerHub account). Any user can easily run the docker image either on the command line or on Deploit (see more details below)

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

Nextflow is a programming language used to build data pipelines that has been widely adopted by the bioinformatics community. It was used here because of it's in-built support for Docker containers and parallelisation that allows the conversion of each of the ECW files to take place simultaneously.

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

The `--input_folder` is a required parameter. It must contain all of the input zipped ecw files to be unzipped and the ecw files converted. The data can be set by clicking the blue database button and selecting your data either from an S3 bucket or by uploading the data. 


![run_nextflow_job](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/run_nextflow_job.png)

#### Setting resources

Select a project & instance:

![instance_nextflow](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/instance_nextflow.png)

## Cost estimate
Resources used for four zipped ecw files, 4.35GB in total (see the job [here](https://deploit.lifebit.ai/public/jobs/5ca8cf0fe4365600b2b15a2e))
* Resources: an m2.2xlarge (spot) instance was used. (This has 4 CPUs & 34.2 GB memory)
* Run time: 2h 46m
* Cost: $0.43

As the bucket contains 2056GB the cost to convert all of the files (assuming the cost scales linearly) may be around $200 (0.426 / 4.35 x 2056)

As the file conversion can be run in parrallel for each of the files (by using the Nextflow pipeline) the total time taken should be equal to that of the time taken to convert the largest file. 

![job_monitor](https://raw.githubusercontent.com/lifebit-ai/ecw-converter/master/images/job_monitor.png)

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

When running the Nextflow pipeline only the `tif` & `img` directories are outputted to save storage space.

When run over Deploit results are made in the users S3 bucket generated by Deploit. This will be located in `s3://lifebit-user-data-<user_id>/results/job-<job_id>/results/` as shown by Deploit
