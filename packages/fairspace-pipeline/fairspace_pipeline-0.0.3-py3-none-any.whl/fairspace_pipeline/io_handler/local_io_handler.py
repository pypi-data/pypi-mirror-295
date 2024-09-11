"""
This module contains classes and functions for running Fairspace pipelines locally. It includes classes
for processing source files, writing ttl files, and uploading data to Fairspace.

Classes:
    LocalIOHandler: Class to handle running pipeline locally.

"""
import glob
import json
import logging
import os
import pathlib
import sys
from typing import List
from rdflib import Graph

from fairspace_pipeline.api_client.fairspace_api_client import FairspaceApi
from fairspace_pipeline.graph.fairspace_graph import FairspaceGraph
from fairspace_pipeline.io_handler.io_handler_interface import IOHandlerInterface

log = logging.getLogger('local_io_handler')


class LocalIOHandler(IOHandlerInterface):
    """
    Handles local input/output operations for Fairspace integration.
    """
    def __init__(self, output_data_directory: str, fairspace_graph: FairspaceGraph):
        super().__init__(fairspace_graph)
        self.output_data_directory = output_data_directory
        self.file_suffix_processing_order = fairspace_graph.get_file_suffix_processing_order()
        self.output_suffix_processing_order = [suffix.replace(".json", ".ttl") for suffix in self.file_suffix_processing_order]


    def transform_data(self, source_directories: str, source_prefixes: List[str] = [""]):
        try:
            for label_prefix in source_prefixes:
                if label_prefix != "":
                    log.info(f'Applying label prefix: "{label_prefix}".')
                for directory in source_directories:
                    for file_suffix in self.file_suffix_processing_order:
                        self.process_entity_file(directory, file_suffix, label_prefix)
                    self.process_entity_file(directory, "", label_prefix)
                    log.info(f'Done processing source files in {directory} folder.')
        except Exception as e:
            log.error(e)
            sys.exit(1)
        log.info(f'Done processing all the source files for configured study directories.')

    def send_to_api(self, api: FairspaceApi):
        for directory, subdirectories, files in os.walk(self.output_data_directory):
            # Order of processing is important, needs to match the defined suffixes order
            for suffix in self.output_suffix_processing_order:
                files_with_suffix = [f for f in files if f.endswith(suffix)]
                self.upload_files_to_fairspace(api, directory, files_with_suffix)
            files_without_suffix = [f for f in files if not any(f.endswith(suffix) for suffix in self.output_suffix_processing_order)]
            self.upload_files_to_fairspace(api, directory, files_without_suffix)
        log.info(f"Done uploading all metadata from {self.output_data_directory} to Fairspace.")

    def write_to_ttl(self, graph: Graph, filename: str, output_directory: str, prefix: str = ""):
        new_file_name = prefix + pathlib.Path(filename).with_suffix('.ttl').name
        output = os.path.join(output_directory, new_file_name)
        graph.serialize(destination=output, format="turtle")
        log.info('Data saved to: ' + output)

    def upload_files_to_fairspace(self, api: FairspaceApi, directory: str, files: list[str]):
        for file_name in files:
            try:
                full_path = os.path.join(directory, file_name)
                log.info(f"Start uploading file {full_path} to Fairspace")
                api.upload_metadata_by_path(full_path)
            except Exception as e:
                log.error(f"Error uploading file {file_name}")
                log.error(e)
                sys.exit(1)

    def process_entity_file(self, source_directory: str, file_suffix: str, file_prefix: str):
        if file_suffix in self.fairspace_graph.get_file_suffix_processing_order():
            self.process_special_entity_file(source_directory, file_suffix, file_prefix)
        else:
            self.process_regular_file(source_directory, file_prefix)

    def process_special_entity_file(self, source_directory, file_suffix, file_prefix):
        entity_files = glob.glob(source_directory + "/*" + file_suffix)
        if len(entity_files) < 1:
            raise Exception(f"File with suffix {file_suffix} not found in the source data directory.")
        if len(entity_files) > 1:
            raise Exception(f"More than one file with suffix {file_suffix} found in the source data directory. "
                            "This is currently not supported. Please specify a single file")
        unique_entity_file_path = entity_files[0]
        try:
            log.info(f"Processing file: {unique_entity_file_path}")
            data = self.read_json(unique_entity_file_path)
            entity_graph = self.fairspace_graph.create_graph(unique_entity_file_path, data, file_prefix)
            self.write_to_ttl(entity_graph, unique_entity_file_path, self.output_data_directory, file_prefix)
        except Exception as e:
            log.error(f"Error processing file: {unique_entity_file_path}")
            raise Exception(e)

    def process_regular_file(self, data_directory: str, prefix: str):
        for directory, subdirectories, files in os.walk(data_directory):
            for file in sorted(files):
                if not any(str(file).endswith(suffix) for suffix in self.file_suffix_processing_order):
                    try:
                        full_path = os.path.join(directory, file)
                        folder_file_path = os.path.join(os.path.basename(directory), file)
                        log.info(f"Processing file with name: {file}")
                        data = self.read_json(full_path)
                        data_graph = self.fairspace_graph.create_graph(folder_file_path, data, prefix)
                        self.write_to_ttl(data_graph, file, self.output_data_directory, prefix)
                    except Exception as e:
                        log.error(f"Error processing file with name {file}")
                        raise Exception(e)

    def read_json(self, file_path: str):
        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                return data
        except Exception as e:
            log.error('Error reading source file content: ' + str(e))
            return None