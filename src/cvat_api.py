import os
import zipfile

import cvat_sdk.api_client
from cvat_sdk import make_client

from typing import Dict, Any


def upload_datasets_from_cvat(config_dict: Dict[str, Any]):
    """
    Simple api request to download datasets from cvat

    :param config_dict: to generate config_dict see src.utils.definition.ConfigParser and config.yaml
    """

    host = config_dict['CVAT_URL'].rstrip('/')
    login = config_dict['LOGIN']
    password = config_dict['PASS']

    downloads_directory = config_dict['SAVE_PATH']
    if not os.path.exists(downloads_directory):
        os.makedirs(downloads_directory, exist_ok=True)

    with make_client(host, credentials=(login, password)) as client:
        for task_id in config_dict['TASKS_IDS']:
            task_info = client.tasks.retrieve(int(task_id))

            archive_path = os.path.join(downloads_directory, str(task_id) + '.zip')
            if os.path.exists(archive_path):
                os.remove(archive_path)

            print(f'downloading "{archive_path}"')

            try:
                task_info.export_dataset('Datumaro 1.0', archive_path)
            except Exception as e:
                print(f'failed to download "{archive_path}": {e})')
                continue

            print(f'successfully downloaded "{archive_path}"')

            target_directory = os.path.join(downloads_directory, str(task_id))
            os.makedirs(target_directory, exist_ok=True)

            print(f'deflating "{archive_path}" to "{target_directory}"')

            try:

                with open(archive_path, 'rb') as zip_input:
                    dataset_zip = zipfile.ZipFile(zip_input)
                    dataset_zip.extractall(target_directory)
            except Exception as e:
                print(f'failed to deflate "{archive_path}": {e}')
                os.remove(archive_path)
                continue

            print(f'successfully deflated "{archive_path}" to "{target_directory}"')

            os.remove(archive_path)
