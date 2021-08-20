Note: The Load Composition Analysis tools are currently under development.

The load composition analysis tool is designed to be used with OpenFIDO.  To install OpenFIDO see http://help.openfido.org/.

## Getting Started

The standard pipeline configuration is as follows:

- Pipeline Name: `NERC Load Composition`

- Description: `The load composition analysis tool provides composite load model (CLM) data for cities in NERC's annual planning studies.`

- DockerHub Repository: `python:3`

- Git Clone URL (https): `https://github.com/slacgismo/load_composition_analysis`

- Repository Branch: `master`

- Entrypoint Script (.sh): `openfido.sh`

The run configuration file is named `config.csv` and uses the following format. The values shown are all those currently supported.  Omitting a value indicates that all valid values are to be used.

~~~
City,ABI ALB AMA ATL AUS BDL BDR BFL BNA BOS BTW BUF BWI CHS CLE CLT CRP CRW CYS DEN DFW DLH DTW ECG FAR GAI GEI GRB IAH JAX LAX LIT MAG MCI MIA MKE MSG MSP MSY NYC OKC OMA ONT ORG ORH PDX PHL PHX PIT PSP PVD PWM RST SAT SDF SEA SFO SLC SMF SPS STL SYR TYR YFC YHZ YOW YQB YQT YSB YUL YUY YYC YYZ YZV
Feeder,Residential Commercial Mixed Rural
Season,Summer Spring Winter
Intermediate Results,weather loadshape
~~~

## Background

The [[/Methodology/Overview]] document provides a high-level discussion of the Load Composition Analysis tools and the results obtained using these tools.

The [[/Methodology/Details]] document provides an in-depth discussion of the procedures and algorithms used in the Load Composition Analysis tools.

The code is documented and demonstrated in the source folder.  See the Jupyter notebooks in the [source folder](https://github.com/slacgismo/load_composition_analysis/tree/master/src) for details.


## Local development

#### Entrypoint:

From the head of the repo, run:

```bash
$ python src/scripts/composite_loads
```

This will default to running the script with /autotest/config.csv. In order to modify the input, create a new config.csv file with the same format and re run the code.

#### Pre-Commit

We make use of the pre-commit hooks to ensure pep8 standards. To activate the pre-commit hook run:

```bash
$ pip install pre-commit
$ pre-commit install
```

Upon running the script locally, ensure the newly created files are not being pushed to the github repo.
