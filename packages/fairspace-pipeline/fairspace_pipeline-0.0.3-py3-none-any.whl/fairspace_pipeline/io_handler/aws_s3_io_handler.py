"""
This module contains classes and functions for running Fairspace pipelines on AWS S3 buckets. It includes classes
for processing source files, writing ttl files, and uploading data to Fairspace.

Classes:
    AwsS3IOHandler: Class to handle running pipeline on AWS S3 buckets.

"""

import json
import logging
import pathlib
import sys
from typing import List

import boto3
from botocore.exceptions import NoCredentialsError
from rdflib import Graph

from fairspace_pipeline.api_client.fairspace_api_client import FairspaceApi
from fairspace_pipeline.graph.fairspace_graph import FairspaceGraph
from fairspace_pipeline.io_handler.io_handler_interface import IOHandlerInterface

log = logging.getLogger('aws_s3_connector')

DEFAULT_BUCKET_PAGINATION_PAGE_SIZE = 10
STAGING_DIRECTORY_NAME = "fairspace-metadata-upload-staging"


class AwsS3IOHandler(IOHandlerInterface):
    """
    IOHandler implementation for interacting with AWS S3.

    This class provides methods for extraction, transformation and loading of data while interacting with AWS S3 bucket.
    """
    def __init__(self, source_bucket_name: str, output_bucket_name: str, fairspace_graph: FairspaceGraph, encoding = 'utf-8-sig'):
        super().__init__(fairspace_graph)
        session = boto3.Session(profile_name='default')
        self.s3_client = session.client('s3')
        self.source_bucket_name = source_bucket_name
        self.output_bucket_name = output_bucket_name
        self.encoding = encoding
        self.file_suffix_processing_order = fairspace_graph.get_file_suffix_processing_order()
        self.output_suffix_processing_order = [suffix.replace(".json", ".ttl") for suffix in self.file_suffix_processing_order]

    def transform_data(self, source_directories: str, source_prefixes: List[str] = []):
        try:
            for label_prefix in source_prefixes:
                if label_prefix != "":
                    log.info(f'Applying label prefix: "{label_prefix}".')
                for source_directory in source_directories:
                    data_path = f"{STAGING_DIRECTORY_NAME}/{label_prefix+source_directory}"
                    self.upload_to_aws(data_path + '/')
                    for file_suffix in self.file_suffix_processing_order:
                        self.process_entity_file(source_directory, file_suffix, label_prefix)
                    self.process_entity_file(source_directory, "", label_prefix)
                    log.info(f'Done processing source files in {source_directory} folder.')
        except Exception as e:
            log.error(e)
            sys.exit(1)
        log.info(f'Done processing all the source files for configured directories.')

    def send_to_api(self, api: FairspaceApi, data_directories: list[str]):
        for data_path in data_directories:
            # Order of processing is important, needs to match the defined suffixes order
            for suffix in self.output_suffix_processing_order:
                study_manifest_files = self.get_files_by_suffix(self.output_bucket_name, data_path, 1, suffix)
                self.upload_file_to_fairspace(api, list(study_manifest_files)[0]['Key'])
            # Upload the rest of the files (paginated) that do not have a suffix
            self.upload_files_to_fairspace_with_pagination(api, data_path)
        log.info(f"Done uploading all metadata from {self.output_bucket_name} bucket to Fairspace.")

    def write_to_ttl(self, graph: Graph, filename: str, output_directory: str, prefix: str = ""):
        new_file_name = prefix + pathlib.Path(filename).with_suffix('.ttl').name
        output = output_directory + "/" + new_file_name
        file = graph.serialize(format="turtle")
        self.upload_to_aws(output, file)

    def upload_files_to_fairspace_with_pagination(self, api: FairspaceApi, data_path: str):
        page_iterator = self.read_from_aws(self.output_bucket_name, data_path,
                                           DEFAULT_BUCKET_PAGINATION_PAGE_SIZE)
        for page in page_iterator:
            log.info(f"Getting {DEFAULT_BUCKET_PAGINATION_PAGE_SIZE} files from S3 {data_path} directory")
            files = page.get("Contents")
            for file in files:
                file_name = file['Key']
                if not any(file_name.endswith(suffix) for suffix in self.file_suffix_processing_order) and not str(
                        file_name).endswith("/"):
                    self.upload_file_to_fairspace(api, file_name)

    def upload_file_to_fairspace(self, api: FairspaceApi, file_name: str):
        try:
            log.info(f"Start uploading file {file_name} to Fairspace")
            file_content = self.get_file_content(self.output_bucket_name, file_name)
            api.upload_metadata('turtle', file_content, False)
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
        entity_files = self.get_files_by_suffix(self.source_bucket_name, source_directory, 1, file_suffix)
        if len(entity_files) < 1:
            raise Exception(f"File with suffix {file_suffix} not found in the source data directory.")
        if len(entity_files) > 1:
            raise Exception(f"More than one file with suffix {file_suffix} found in the source data directory.")
        entity_file_name = entity_files[0]['Key']
        try:
            log.info(f"Processing file: {entity_file_name}")
            file_content = self.get_file_content(self.source_bucket_name, entity_file_name)
            data = json.loads(file_content)
            special_entity_graph = self.fairspace_graph.create_graph(entity_file_name, data, file_prefix)
            data_path = f"{STAGING_DIRECTORY_NAME}/{file_prefix}{source_directory}"
            self.write_to_ttl(special_entity_graph, entity_file_name, data_path, file_prefix)
        except Exception as e:
            log.error(f"Error processing file with name {entity_file_name}")
            raise Exception(e)

    def process_regular_file(self, data_directory: str, prefix: str):
        page_iterator = self.read_from_aws(self.source_bucket_name, data_directory, DEFAULT_BUCKET_PAGINATION_PAGE_SIZE)
        page_count = 0
        for page in page_iterator:
            log.info(f"Getting {DEFAULT_BUCKET_PAGINATION_PAGE_SIZE} files from page {page_count} of {data_directory}...")
            files = page.get("Contents")
            page_count = page_count+1
            for file in files:
                file_path = file['Key']
                try:
                    log.info(f"Processing file with name: {file_path}, size: {file['Size']}")
                    file_content = self.get_file_content(self.source_bucket_name, file_path)
                    data = json.loads(file_content)
                    data_graph = self.fairspace_graph.create_graph(file_path, data, prefix)
                    data_path = f"{STAGING_DIRECTORY_NAME}/{prefix + data_directory}"
                    self.write_to_ttl(data_graph, file_path, data_path, prefix)
                except Exception as e:
                    log.error(f"Error processing file with name {file_path}")
                    raise Exception(e)

    def upload_to_aws(self, s3_object_name: str, object_to_upload=None):
        try:
            if object_to_upload is not None:
                self.s3_client.put_object(Body=object_to_upload, Bucket=self.output_bucket_name, Key=s3_object_name)
            else:
                self.s3_client.put_object(Bucket=self.output_bucket_name, Key=s3_object_name)
            log.info(f"Successfully uploaded {s3_object_name} to {self.output_bucket_name} AWS S3 bucket.")
            return True
        except NoCredentialsError:
            log.error("AWS S3 bucket credentials not available.")
            raise Exception(NoCredentialsError)
        except Exception as e:
            log.error(f"Error uploading {s3_object_name} to {self.output_bucket_name} AWS S3 bucket.")
            raise Exception(e)

    def read_from_aws(self, bucket_name: str, path: str, page_size: int):
        paginator = self.s3_client.get_paginator("list_objects_v2")
        return paginator.paginate(Bucket=bucket_name, Prefix=path, PaginationConfig={"PageSize": page_size})

    def get_files_by_suffix(self, bucket_name: str, path: str, page_size: int, suffix: str):
        page_iterator = self.read_from_aws(bucket_name, path, page_size)
        files = page_iterator.search(f"Contents[?ends_with(Key, `{suffix}`)][]")
        return files

    def get_file_content(self, bucket_name: str, file_key: str):
        file_object = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = file_object['Body'].read().decode(self.encoding, errors="ignore")
        return file_content
