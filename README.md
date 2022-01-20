## INTRODUCTION

This repository contains code to:

- Download Landsat imagery from Amazon Web Services open data repository for the San Francisco area
- Download OpenStreetMap road data for San Francisco (tagged 'San Francisco')
- Create RGB composite raster from Landsat data, with additional pan-sharpening (_**tci.jpg**_)
- Create bounding box and clip RGB composite raster
- Create a map zoomed in to San Francisco city with overlain road network (_**map.jpg**_)
- Dockerize all related code items described above
- Perform unit testing of all related code items described above

It was developed in Linux through WSL2 (Ubuntu 20.04) on a Windows10 machine, and tested on Linux and Windows 10 (powershell), so all of it should run fine on either of these systems. It is likely to run fine on MacOS as well, but this has not been tested.

Total processing time on a standard PC is approximately 3 minutes. Depending on the system, this can be less or more. If it is running longer than 10 minutes, please check internet speeds and/or try on a different machine.

The code creates two directories in its working directory: _**tmp**_ and _**out**_:

- The _**tmp**_ directory contains all data that was used to create the required products; this includes satellite imagery and vector data.

- The _**out**_ directory contains the two data products, **tci.jpg** and **map.jpg**.

Please note, that the road network shown in **map.jpg** only covers San Francisco proper until the county borders. Because of that, it does not extent fully in the lower (southern) part of the image.

## HOW TO RUN

### Docker

This build process has been tested on Linux via WSL2 and Windows 10 (cmd; powershell).

To build the Docker image, run the following command from within the repository:

```bash
docker build -t roadmap .
```

The test suite will run during the build process, using _**pytest**_. If it fails, the Docker image build will fail as well. Please open an issue if this happens.

Once the build process is complete, run the Docker image with the following command:

```bash
docker run --rm -i -v ${PWD}:/app -e AWS_ACCESS_KEY_ID=<access-key-id> -e AWS_SECRET_ACCESS_KEY=<secret-access-key> roadmap
```

Please do not forget to replace "access-key-id" and "secret-access-key" with valid AWS credentials. Without these, the program will download a backup file from my dropbox. 

### Testing

The test suite is run during the build process of the docker image. However, it can also be directly invoked by running _**pytest**_ from within the main directory of the repo.

If run outside of docker, the test suite requires an existing conda environment. This environment can be created using the conda _environment.yml_ file present in the repository. The easiest way to get a working conda installation is by installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Once conda is installed, run the following command to create a new conda environment:

```bash
conda env create -f environment.yml
```

Activate the conda environment by running:

```bash
conda activate roadmap
```

Once the environment is activated, run the following command from the main folder of the repository, to start the testing suite:

```bash
pytest
```

### Bash

If the conda environment has been created, the code can also be run directly:

```bash
python solution.py
```

## DATA SOURCES

- Landsat 8 imagery courtesy of the [U.S. Geological Survey](https://www.usgs.gov)

- OpenStreetMap data courtesy of OpenStreetMap contributors, and available via [OpenStreetMap.org](https://www.openstreetmap.org), license under the [Open Data Commons](https://opendatacommons.org/licenses/odbl/) license.
