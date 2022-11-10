# Upload data from cvat

## Description

Simple downloading datasets from CVAT.
Easy preparing dataset to training and testing.
Overview of functionality:
- Download datasets from CVAT (supports all formats via format string)
- Combining tasks into a single dataset
- Random split of a dataset into a training subset, validation subset and test subset


## Installation

```bash
1.    sudo pip3.8 install virtualenv
```
```bash
2.    python3.8 -m venv venv
```
```bash
3.    source venv/bin/activate
```
```bash
4.    pip3 install -r requirements.txt
```

## Usage

It is recommended to use a configuration file rather than command-line arguments.
Open [config_file](config.yaml)

```yaml
# url
CVAT_URL: 'url/to/cvat'

# auth
LOGIN: 'login'
PASS: 'password'

# tasks to download
TASKS_IDS: '156,157,158,159,160,161,162,163,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284'

# final format of dataset
EXPORT_FORMAT: 'coco'

# path to save dataset
SAVE_PATH: 'path/to/save/dataset'

# Random split of a dataset into a training subset, validation subset, and test subset
SPLIT_DATASET: 'train:.8,val:.1,test:.1' # the sum of the shares must be equal to 1.0

# Turns on / off only building dataset, if the tasks is already loaded   
ONLY_BUILD_DATASET: ''

```

```bash
python3 main.py
```

To use command line:

```bash
usage: main.py [-h] [--auth USER:[PASS]] [--cvat_url CVAT_URL] [--tasks_ids TASKS_IDS] [--export_format EXPORT_FORMAT]
               [--save_path SAVE_PATH] [--split_dataset SPLIT_DATASET] [--use_command_line USE_COMMAND_LINE]
               [--only_build_dataset ONLY_BUILD_DATASET]

Perform common operations related to CVAT tasks.

optional arguments:
  -h, --help            show this help message and exit
  --auth USER:[PASS]    defaults to the current user and supports the PASS environment variable or password prompt (default
                        user: admin:admin).
  --cvat_url CVAT_URL   url of the CVAT
  --tasks_ids TASKS_IDS
                        tasks to download. Example: "233,555,222"
  --export_format EXPORT_FORMAT
                        dataset format, for more info check CVAT docs
  --save_path SAVE_PATH
                        path to save downloaded datasets
  --split_dataset SPLIT_DATASET
                        randomly splits dataset on train, val and test subsets
  --use_command_line USE_COMMAND_LINE
                        Use commad line or config file
  --only_build_dataset ONLY_BUILD_DATASET
                        Turns on / off only building dataset, if the tasks is already loaded  
```

To use API see [cvat_api.py](src/cvat_api.py)
