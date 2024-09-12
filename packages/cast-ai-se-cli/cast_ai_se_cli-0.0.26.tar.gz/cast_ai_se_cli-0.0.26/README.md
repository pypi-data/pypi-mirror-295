# CAST AI SE CLI (cast-ai-se-cli package | se-cli tool)

[![PyPI version](https://img.shields.io/pypi/v/my-awesome-package.svg)](https://pypi.org/project/cast-ai-se-cli/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-000000.svg)](https://flake8.pycqa.org/)

[![GitHub Issues](https://img.shields.io/github/issues/castai/solutions-engineering-lab)](https://github.com/castai/solutions-engineering-lab/issues)
[![GitHub release](https://img.shields.io/github/release/castai/solutions-engineering-lab)](https://github.com/castai/solutions-engineering-lab/releases)

## Introduction / Overview

This project aims to serve as swiss knife intended to serve CAST AI SEs.
Assisting with demo environment prep, providing snapshot analysis and many others in the future.
The CLI tool is based on a modular architecture and leverages API orchestration tools package -> cast-ai-se-tools

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install, run:\
    `pip install cast-ai-se-cli`\
or forced:\
    `pip install cast-ai-se-cli --force-reinstall`

To upgrade, run:\
    `pip install --upgrade cast-ai-se-cli` \
or forced:\
    `pip install --upgrade --force-reinstall cast-ai-se-cli`

## Usage

For some of the functions(commands) the tool offers a configuration file is required (config.json).\
First time running the tool if file is not found, the tool would create an empty template file.\
The user is required to fill fields required to automate sequences related to the chosen command. \
The template comes with additional default parameters that can found [here](config_constants.py)


### High-Level:
### CLI commands:
    se-cli demo <prep|off> <eks|aks|gcp> [--cluster_id <cluster_id>] [-h|--help] [-d|--debug]
    se-cli snapshot <analyze> <brief|detailed> [--cluster_id <cluster_id>] [-h|--help] [-d|--debug]
    se-cli audit <analyze> [--cluster_id <cluster_id>] [-h|--help] [-d|--debug]
#### CLI commmands explained:
    se-cli demo <prep|off> <eks|aks|gcp>
- demo command is used to either **prep** a demo environment:\
Use the config.json data to get the cluster into a specific node count (default=7) \
with specific replicated demo replicas (default=2) and then delete previous nodes
Turning **off** a cluster would be invoking the hibernation cronjob.

- The subcommand **<eks|aks|gcp>** is to determine which cluster will be prep`ed or turned off.\

 
    se-cli snapshot <analyze> <brief|detailed>

- snapshot command is used to either generate a **brief** or **detailed** report of workloads that have some effect on 
scheduling:
- nodeSelector
- topologySpreadConstraints
- affinity
- runtimeClassName
- pdb`s 

Workloads analyzed:
- deployments
- replicaSets
- daemonSets
- statefulSets
- jobs

The detailed report includes the namespaces and names of workloads
 

### Options:
    -h, --help  Show this help message and exit.
    -d, --debug  Enable debug logging.
    -c, --cluster_id <cluster_id>  (Optional) Specify the cluster ID for the demo environment.

## Command->Outcome:

`se-cli demo prep` :

![Alt Text](images/demo_prep.png)

`se-cli demo off` :

![Alt Text](images/demo_off.png)

Hitting a timeout:

![Alt Text](images/demo_refresh-timeout.png)

`se-cli audit analyze` :

## Contributing

Contributions are welcome! To contribute, follow these steps:

git clone project as first step
create features/fixes by applying a simple <TYPE(fix/feature...)>/<INITIATING_USER>-<FEATURE/FIX-NAME> branch
do not forget to update version and open a PR
Please make sure CI process that enforces light flake8 lint passes (flak8 and other helper script can be found in helper_script folder)

## License

This project is licensed under the [APACHE License](LICENSE).


## Roadmap

- Version 0.1.0: First semi-major release end of 2023 Q4 - tested and vetted demo functionality
- Version 0.2.0: Second semi-major release to support snapshots analysis
- Version 0.3.0: Third semi-major to integrate with solution-engineering tool
- Version 1.0.0: First Major release tested and vetter all other previous releases (end of 2024 Q1)
