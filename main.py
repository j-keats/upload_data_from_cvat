import os
from src.utils.definition import parser, ConfigParser
from src.dataset_builder import CustomDataset
from src.cvat_api import upload_datasets_from_cvat


def main():
    args = parser.parse_args()
    config_dict = ConfigParser().get_config_dict()
    
    map_list = [('text', 'text')]

    if args.use_command_line:
        print('Using command line interface\n')
        config_dict = ConfigParser().args_matcher(args, config_dict)
    else:
        print('Using config file\n')

    if not config_dict['ONLY_BUILD_DATASET']:
        print('Start downloading tasks\n')
        upload_datasets_from_cvat(config_dict)

    if os.path.exists(config_dict['SAVE_PATH']):
        print('Start buiding dataset\n')
        dataset = CustomDataset(datasets_path=config_dict['SAVE_PATH'], 
                                export_format=config_dict['EXPORT_FORMAT'])
        dataset.transform_dataset(splits=config_dict['SPLIT_DATASET'], 
                                  mapping=map_list)
    else:
        raise Exception('Tasks are not loaded!')


if __name__ == '__main__':
    main()


