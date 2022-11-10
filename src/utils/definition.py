# SPDX-License-Identifier: MIT
import argparse
import getpass
import os
import yaml


class ConfigParser():

    def __init__(self, config_file_path:str='config.yaml'):
        self.config_file_path = config_file_path
    
    def get_config_dict(self):
        with open(self.config_file_path) as config_file:
            self.conf_dict = yaml.safe_load(config_file)
        
        self.conf_dict['TASKS_IDS'] =  self.parse_tasks(self.conf_dict['TASKS_IDS'])
        self.conf_dict['SPLIT_DATASET'] = self.parser_splits(self.conf_dict['SPLIT_DATASET'])

        return self.conf_dict
    
    def args_matcher(self, args, config_dict):

        config_dict['CVAT_URL'] = args.cvat_url
        config_dict['LOGIN'] = args.auth[0]
        config_dict['PASS'] = args.auth[1]
        config_dict['TASKS_IDS'] = self.parse_tasks(args.tasks_ids)
        config_dict['EXPORT_FORMAT'] = args.export_format
        config_dict['SAVE_PATH'] = args.save_path
        config_dict['SPLIT_DATASET'] = self.parser_splits(args.split_dataset)
        config_dict['ONLY_BUILD_DATASET'] = args.only_build_dataset
        
        return config_dict

    @staticmethod
    def parse_tasks(s):
        tasks = s.split(',')
        return tasks

    @staticmethod
    def parser_splits(s):
        splits = []
        datasets = s.split(',')
        for dataset_line in datasets:
            subset = dataset_line.split(':')[0]
            num = float(dataset_line.split(':')[1])
            splits.append(tuple([subset, num]))
        
        return splits


def get_auth(s:str):
    """ 
    Parse USER[:PASS] strings and prompt for password if none was
    supplied. 
    """

    user, _, password = s.partition(':')
    password = password or os.environ.get('PASS') or getpass.getpass()
    return user, password


def parse_tasks(s:str):
    tasks = s.split(',')
    return tasks

def parser_splits(s:str):

    splits = []
    datasets = s.split(',')
    for dataset_line in datasets:
        subset = dataset_line.split(':')[0]
        num = float(dataset_line.split(':')[1])
        splits.append(tuple(subset, num))
    
    return splits

#######################################################################
# Command line interface definition
#######################################################################

parser = argparse.ArgumentParser(
    description='Perform common operations related to CVAT tasks.\n\n'
)

parser.add_argument(
    '--auth',
    type=get_auth,
    metavar='USER:[PASS]',
    default='admin:Secure1337!#',
    help='''defaults to the current user and supports the PASS 
            environment variable or password prompt (default user: %(default)s).'''
)

parser.add_argument(
    '--cvat_url',
    type=str,
    default='https://xray-cvat.neuro-vision.tech',
    help='url of the CVAT'
)

parser.add_argument(
    '--tasks_ids',
    type=str,
    default='',
    help='tasks to download. Example: "233,555,222"'
)

parser.add_argument(
    '--export_format',
    type=str,
    default='coco', 
    help='dataset format, for more info check CVAT docs'
)

parser.add_argument(
    '--save_path', 
    type=str,
    default='datasets',
    help='path to save downloaded datasets'
)

parser.add_argument(
    '--split_dataset',
    type=str,
    default='train:1.0, val:.0, test:.0',
    help='randomly splits dataset on train, val and test subsets'
)

parser.add_argument(
    '--use_command_line',
    type=bool,
    default=False,
    help='Use commad line or config file'
)

parser.add_argument(
    '--only_build_dataset',
    type=bool,
    default=False,
    help='Flag includes only the functionality of building a dataset if the tasks are already loaded'
)