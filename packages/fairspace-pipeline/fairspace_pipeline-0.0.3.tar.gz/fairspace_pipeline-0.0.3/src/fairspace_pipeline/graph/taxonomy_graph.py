import logging
from typing import Optional

from rdflib import Graph

log = logging.getLogger('taxonomy_graph')


class TaxonomiesGraph:
    """
    Represents a graph of taxonomies for querying and looking up terms.
    """

    def __init__(self, taxonomies_dir: str, taxonomy_prefix: str = 'https://fairspace.nl/ontology#'):
        self.taxonomies_graph = Graph()
        self.taxonomies_graph.parse(taxonomies_dir, format='ttl')
        self.taxonomy_prefix = taxonomy_prefix

    def query_taxonomy(self, taxonomy_name: str, label: str = 'rdfs:label') -> dict:
        query = f"""
            PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX prefix: <{self.taxonomy_prefix}>

            SELECT ?id ?label
            WHERE {{
                ?id a prefix:{taxonomy_name} .
                ?id {label} ?label
            }}
        """
        return {subject['id']: subject['label'].toPython() for subject in self.taxonomies_graph.query(query).bindings}

    def lookup_term(self, term: str, taxonomy_reference: dict) -> Optional[str]:
        try:
            lower_values = {val.lower(): key for key, val in taxonomy_reference.items()}
            return lower_values.get(term.lower())
        except Exception as e:
            log.error(e)
            return None
