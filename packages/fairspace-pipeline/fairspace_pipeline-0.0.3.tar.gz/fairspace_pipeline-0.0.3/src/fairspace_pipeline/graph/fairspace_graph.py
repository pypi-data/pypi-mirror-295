import logging
from typing import Optional, List
from rdflib import Graph

from fairspace_pipeline.graph.taxonomy_graph import TaxonomiesGraph

log = logging.getLogger('fairspace_graph')


class FairspaceGraph:

    def __init__(self, taxonomies_graph: TaxonomiesGraph):
        self.taxonomy_graph = taxonomies_graph

    def create_new_graph(self, namespaces={}) -> Graph:
        g = Graph()
        for prefix, namespace in namespaces.items():
            g.bind(prefix, namespace)
        return g

    def lookup_taxonomy_term(self, term, taxonomy_ref) -> Optional[str]:
        if term is not None:
            return self.taxonomy_graph.lookup_term(term, taxonomy_ref)
        return

    def get_value_by_one_of_keys(self, source, keys: List[str]):
        for key in keys:
            value = source.get(key)
            if value is not None:
                return value

    def create_graph(self, file_path: str, data, prefix: str):
        pass
