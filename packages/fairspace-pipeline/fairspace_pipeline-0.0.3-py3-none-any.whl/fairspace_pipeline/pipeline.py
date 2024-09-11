import logging
import sys

from fairspace_pipeline.api_client.fairspace_api_client import FairspaceApi
from fairspace_pipeline.graph.fairspace_graph import FairspaceGraph
from fairspace_pipeline.io_handler.aws_s3_io_handler import AwsS3IOHandler
from fairspace_pipeline.io_handler.local_io_handler import LocalIOHandler
from fairspace_pipeline.io_handler.io_handler_interface import IOHandlerInterface

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger('pipeline_main')


class FairspacePipelineConfig:
    def __init__(self):
        self.source_study_prefixes: str = '[""]'
        self.output_data_directory: str = None
        self.is_aws_s3: bool = False
        self.source_study_directories = []
        self.source_bucket_name: str = None
        self.output_bucket_name: str = None
        self.taxonomies_directory: str = None
        self.fairspace_api_url: str = None
        self.keycloak_server_url: str = None
        self.keycloak_realm: str = None
        self.keycloak_client_id: str = None
        self.keycloak_client_secret: str = None
        self.keycloak_username: str = None
        self.keycloak_password: str = None
        self.verify_cert: bool = True


class FairspacePipeline:
    def __init__(self, config: FairspacePipelineConfig, fairspace_graph: FairspaceGraph, custom_io_handler: IOHandlerInterface=None):
        self.config = config
        self.fairspace_graph = fairspace_graph

        if custom_io_handler:
            self.io_handler = custom_io_handler
        elif self.config.is_aws_s3:
            self.io_handler = AwsS3IOHandler(self.config.source_bucket_name, self.config.output_bucket_name, fairspace_graph)
        else:
            self.io_handler = LocalIOHandler(self.config.output_data_directory, fairspace_graph)

        try:
            self.api = FairspaceApi(self.config.fairspace_api_url, self.config.keycloak_server_url,
                                    self.config.keycloak_realm, self.config.keycloak_client_id,
                                    self.config.keycloak_client_secret, self.config.keycloak_username,
                                    self.config.keycloak_password, self.config.verify_cert)
        except Exception as e:
            log.error(e)
            sys.exit(1)

    def prepare_current_user(self):
        user = self.api.get_current_user()
        self.api.update_user(user['id'], {'canQueryMetadata': 'true', 'canAddSharedMetadata': 'true'})

    def upload_taxonomies_to_fairspace(self):
        log.info('Updating taxonomies...')
        self.api.upload_metadata_by_path(self.config.taxonomies_directory)

    def reindex(self):
        log.info('Triggering recreation of a view database from the RDF database...')
        self.api.reindex()
        log.info("Reindexing started!")

    def run(self, init: bool = False, process: bool = False, upload: bool = False, delete: bool = False,
            reindex: bool = False, compact: bool = False, check_maintenance_status: bool = False):
        if init:
            self.prepare_current_user()
            self.upload_taxonomies_to_fairspace()
        if process:
            self.io_handler.transform_data(self.config.source_study_directories, self.config.source_study_prefixes)
        if upload:
            self.io_handler.send_to_api(self.api, self.config.source_study_directories)
        if delete:
            log.warning("Deletion not yet supported...")
        if reindex:
            self.reindex()
        if compact:
            self.api.compact()
        if check_maintenance_status:
            log.info("Maintenance status: " + self.api.maintenance_status())
        return True
