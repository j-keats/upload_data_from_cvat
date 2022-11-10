import os
from collections import OrderedDict
import json

from datumaro.components.project import Project
from datumaro.components.operations import IntersectMerge
from datumaro.components.errors import QualityError, MergeError


class CustomDataset():

    def __init__(self, datasets_path:str, export_format:str='coco'):
        """
        :param datasets_path: path to folder with tasks in datumaro format
        :param export_format: final format of dataset
        """
        self.export_format = export_format
        self.datasets_path = datasets_path
        self.datasets_names = os.listdir(datasets_path)

    def create_projects(self) -> list:
        """
        Create list of datumaro.datasets from tasks in datumaro format
        """
        source_datasets = []
        for name in self.datasets_names:
            project = Project().import_from(path=os.path.join(self.datasets_path, name),
                                            dataset_format='datumaro')
            source_datasets.append(project.make_dataset())
        return source_datasets
    
    def merge_datasets(self, source_datasets:list=None, export:bool=False):
        """
        Build dataset from tasks without spliting

        :param source_datasets: list of datumaro.datasets, see self.create_projects()
        :param export: if need save dataset in target format without spliting on train, val and test

        :return merger_project: datumaro.project
        :return merger_dataset: datumaro.dataset
        :return merger: datumaro.extractor
        """
        
        if source_datasets is None:
            source_datasets = self.create_projects()
        merger = IntersectMerge(conf=IntersectMerge.Conf(pairwise_dist=0.5, 
                                                         groups=[], 
                                                         output_conf_thresh=0.0, 
                                                         quorum=0)
        )
        merged_dataset = merger(source_datasets)
        merger_project = Project()
        output_dataset = merger_project.make_dataset()
        output_dataset.define_categories(merged_dataset.categories())
        merged_dataset = output_dataset.update(merged_dataset)

        if export:
            merged_dataset.export(save_dir=f'{self.datasets_path}_{self.format}', 
                                  format=self.export_format, 
                                  save_images=True
            )

        return merger_project, merged_dataset, merger
    
    def transform_dataset(self, 
                      splits:list=[('train', 0.67), ('test', 0.33)], 
                      mapping:list=[('bottle', 'bottle'), 
                                    ('folded knife', 'folded knife'), 
                                    ('knife', 'knife'),
                                    ("phone_battery", "phone_battery"),
                                    ("phone", "phone"),
                                    ("gun up", "gun up"),
                                    ("gun side", "gun side"),
                                    ("tablet", "tablet"),
                                    ("cylinderBattery", "cylinderBattery")],
                      project=None, 
                      dataset=None, 
                      merger=None):
                      
        """
        Random split dataset on subsests and filter image without annotations and save it.

        :param splits: list of tuple of spliting discription: ('subset_name': part_of_subset:float). 
        :param mapping: list of tuple of mapping discription: ('source_label': 'target_label').
        :param project: datumaro.project, see self.merge_datasets()
        :param dataset: datumaro.dataset, see self.merge_datasets()
        :param merger: datumaro.extractor, see self.merge_datasets()
        """

        if dataset is None or project is None or merger is None:
            project, dataset, merger = self.merge_datasets()
        
        method_split = project.env.make_transform('random_split')
        method_mapping = project.env.make_transform('remap_labels')

        extractor_split = dataset.transform(method=method_split, 
                                            splits=splits)

        transform_dataset = Project().make_dataset()
        transform_dataset._categories = extractor_split.categories()
        transform_dataset.update(extractor_split)

        extractor_mapping = transform_dataset.transform(method=method_mapping, 
                                                        mapping=mapping,
                                                        default='delete'
        )

        mapping_dataset = Project().make_dataset()
        mapping_dataset._categories = extractor_mapping.categories()
        mapping_dataset.update(extractor_mapping)

        filter_extractor = mapping_dataset.filter(expr='/item/annotation', 
                                                  filter_annotations=True, 
                                                  remove_empty=True
        )

        filter_dataset = Project().make_dataset()
        filter_dataset._categories = filter_extractor.categories()
        filter_dataset.update(filter_extractor)

        filter_dataset.export(save_dir=f'{self.datasets_path}_{self.export_format}_split', 
                              format=self.export_format, 
                              save_images=True
        )
        print(f'Save reworked dataset at {self.datasets_path}_{self.export_format}_split!')
        report_path = os.path.join(f'{self.datasets_path}_{self.export_format}_split', 'merge_report.json')
        self.save_merge_report(merger, report_path)
    
    @staticmethod
    def save_merge_report(merger, path):
        item_errors = OrderedDict()
        source_errors = OrderedDict()
        all_errors = []

        for e in merger.errors:
            if isinstance(e, QualityError):
                item_errors[str(e.item_id)] = item_errors.get(str(e.item_id), 0) + 1
            elif isinstance(e, MergeError):
                for s in e.sources:
                    source_errors[s] = source_errors.get(s, 0) + 1
                item_errors[str(e.item_id)] = item_errors.get(str(e.item_id), 0) + 1

            all_errors.append(str(e))

        errors = OrderedDict([
            ('Item errors', item_errors),
            ('Source errors', source_errors),
            ('All errors', all_errors),
        ])

        with open(path, 'w') as f:
            json.dump(errors, f, indent=4)
        

            