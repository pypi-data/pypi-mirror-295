from typing import List

from fairspace_pipeline.api_client.fairspace_api_client import FairspaceApi
from fairspace_pipeline.graph.fairspace_graph import FairspaceGraph


class IOHandlerInterface:
    def __init__(self, fairspace_graph: FairspaceGraph):
        self.fairspace_graph = fairspace_graph

    # Extracts data from the source directories and transforms it into graph data and saves it as TTL files
    def transform_data(self, source_study_directories: List[str], source_study_prefixes: List[str]):
        pass

    # Uploads data to Fairspace by sending the saved TTl files to the Fairspace API
    def send_to_api(self, api: FairspaceApi, source_study_directories: List[str]):
        pass
