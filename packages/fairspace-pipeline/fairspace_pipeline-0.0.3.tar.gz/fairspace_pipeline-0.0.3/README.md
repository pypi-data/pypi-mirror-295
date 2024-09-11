# Fairspace Pipeline

[![PyPI](https://img.shields.io/pypi/v/fairspace_pipeline.svg)](https://pypi.org/project/fairspace_pipeline/)
![PyPI - Status](https://img.shields.io/pypi/status/fairspace_pipeline.svg)
[![Apache 2.0 license](https://img.shields.io/pypi/l/fairspace_pipeline.svg)](LICENSE)

This repository contains the Fairspace Pipeline, 
a package that can be used as a base to create custom ETL pipelines for Fairspace.

## Installation

Requires Python 3.12 or newer.

### Installing from PyPI

```shell
python -m pip install fairspace-pipeline
```

### Installing from sources

```shell
git clone https://github.com/thehyve/fairspace-pipeline.git
python -m build
python -m pip install .
```

## Usage

Fairspace Pipeline cannot be used as a standalone package. It requires a custom implementation of several and specific configuration.
Sections below describe the necessary steps to create a fully-functioning custom pipeline with reusable components and interfaces implementation.

### Configuration
Create a `.env` file with the following environment variables:

```shell
# Keycloak
KEYCLOAK_CLIENT_ID="" # e.g. KEYCLOAK_CLIENT_ID="workspace-client"
KEYCLOAK_CLIENT_SECRET="" # e.g. KEYCLOAK_CLIENT_SECRET="********"
KEYCLOAK_USERNAME="" # e.g. KEYCLOAK_USERNAME="organisation-admin"
KEYCLOAK_PASSWORD="" # e.g. KEYCLOAK_PASSWORD="fairspace123"
KEYCLOAK_SERVER_URL="" # e.g. KEYCLOAK_SERVER_URL="https://my-keycloak-instance.com"
KEYCLOAK_REALM="" # e.g. KEYCLOAK_REALM="fairspace"

# Fairspace
FAIRSPACE_URL="" # e.g. FAIRSPACE_URL="https://my-fairspace-instance.com"

# Amazon S3
IS_AWS_S3=False # e.g. IS_AWS_S3=True if using AWS S3 bucket for source data
AWS_SOURCE_BUCKET_NAME="" # e.g. AWS_SOURCE_BUCKET_NAME="fairspace-metadata-source"
AWS_OUTPUT_BUCKET_NAME="" # e.g. AWS_OUTPUT_BUCKET_NAME="fairspace-metadata-output"

# Pipeline settings
TAXONOMIES_TTL_PATH="config/custom_taxonomies.ttl"
SOURCE_STUDIES_PATHS='' # e.g. '["./test_data/test_study_input1", "./test_data/test_study_input2"]'
OUTPUT_DATA_PATH="" # e.g. OUTPUT_DATA_PATH="./test_data/.output_data"
```

Next, implement a function that creates a FairspacePipelineConfig object using environment variables

```python
def get_config() -> FairspacePipelineConfig:
    config = FairspacePipelineConfig()
    config.source_study_prefixes = json.loads(str(os.environ.get('SOURCE_STUDIES_PREFIXES', '[""]')))
    config.output_data_directory = os.environ.get('OUTPUT_DATA_PATH',
                                                  os.path.join(os.getcwd(), 'test_data/.output_data'))
    config.is_aws_s3 = os.getenv("IS_AWS_S3", 'False').lower() in ('true', '1', 't')
    if config.is_aws_s3:
        config.source_study_directories = json.loads(os.environ.get('SOURCE_STUDIES_PATHS'))
    else:
        config.source_study_directories = [os.path.join(os.getcwd(), val) for val in json.loads(
            os.environ.get('SOURCE_STUDIES_PATHS', '["test_data/source_data"]'))]
    config.source_bucket_name = os.environ.get('AWS_SOURCE_BUCKET_NAME')
    config.output_bucket_name = os.environ.get('AWS_OUTPUT_BUCKET_NAME')
    config.taxonomies_directory = os.environ.get(
        'TAXONOMIES_TTL_PATH',
        os.path.join(pathlib.Path(__file__).parent.absolute(), "config", "taxonomies.ttl")
    )
    return config
```


### Taxonomies
Implement custom taxonomies graph class that extends [the `TaxonomiesGraph` class](src/fairspace_pipeline/graph/taxonomy_graph.py).
The class needs to:
- include all custom taxonomies as class attributes,
- define the TAXONOMY_PREFIX to be used in custom taxonomy terms URIs.

Sample implementation:
```python
from fairspace_pipeline.graph.taxonomy_graph import TaxonomiesGraph

TAXONOMY_PREFIX = "https://fairspace.com/custom_ontology#"  # Prefix for custom taxonomies

class CustomTaxonomiesGraph(TaxonomiesGraph):
    def __init__(self, taxonomies_dir):
        super().__init__(taxonomies_dir, TAXONOMY_PREFIX)
        self.countries = self.query_taxonomy(taxonomy_name='Country')
        self.file_types = self.query_taxonomy(taxonomy_name='FileType')
        self.species = self.query_taxonomy(taxonomy_name='Species')
        self.gender = self.query_taxonomy(taxonomy_name='Gender')
        self.study_status = self.query_taxonomy(taxonomy_name='StudyStatus')
        self.study_phases = self.query_taxonomy(taxonomy_name='StudyPhase')
        self.sample_treatments = self.query_taxonomy(taxonomy_name='Treatment')
```

### Mapping

Implement custom graph class that extends [the `FairspaceGraph` class](src/fairspace_pipeline/graph/fairspace_graph.py). 
It is a module for mapping data to RDF graphs specific to the custom data model, e.g.:

The class needs to implement `create_graph()` and `get_file_suffix_processing_order()` methods of the `FairspaceGraph` interface.

Sample implementation:
```python
from fairspace_pipeline.graph.fairspace_graph import FairspaceGraph

CUSTOM_NS = Namespace("https://custom.com/ontology#")

class CustomGraph(FairspaceGraph):
    def __init__(self, taxonomies_graph: CustomTaxonomiesGraph):
        super().__init__(taxonomies_graph)

    def map_study(self, study_dict: dict) -> Study:
        # Implement custom study processing logic
        pass

    def map_sample(self, sample_dict: dict) -> Sample:
        # Implement custom sample processing logic
        pass

    def map_subject(self, subject_dict: dict) -> Subject:
        # Implement custom subject processing logic
        pass

    def create_study_graph(self, data: dict, prefix: str) -> Graph:
        graph = self.create_new_graph()
        studies = self.map_studies(data, prefix)
        for study in studies:
            graph.add((study.uri, RDF.type, CUSTOM_NS.Study))
            if study.label is not None:
                graph.add((study.uri, RDFS.label, Literal(study.label)))
            if study.identifier is not None:
                graph.add((study.uri, DCTERMS.identifier, Literal(study.identifier)))
            ...
        return graph

    def create_sample_graph(self, data: dict, prefix: str) -> Graph:
        graph = self.create_new_graph()
        samples = self.map_sample(data, prefix)
        for sample in samples:
            ...
        return graph
            
    def create_subject_graph(self, data: dict, prefix: str) -> Graph:
        graph = self.create_new_graph()
        subjects = self.map_subject(data, prefix)
        for subject in subjects:
            ...
        return graph
            
    def create_graph(self, file_path: str, data: dict, prefix: str) -> Graph:
        if str(file_path).endswith(STUDY_MANIFEST_FILE_SUFFIX):
            return self.create_study_graph(data, prefix)
        if str(file_path).endswith(SAMPLE_INFORMATION_SUFFIX):
            return self.create_sample_graph(data, prefix)
        ...
        return self.create_subjects_data_files_graph(data, prefix)

    # Define the order of processing files by file suffix in the source study directory
    # e.g. ['_study.json', '_sample_information.json']
    def get_file_suffix_processing_order(self) -> list[str]:
        return [STUDY_MANIFEST_FILE_SUFFIX, SAMPLE_INFORMATION_SUFFIX]
```

#### Pipeline runner

Define main function to run the pipeline.
```python
from fairspace_pipeline.pipeline import FairspacePipeline, FairspacePipelineConfig

def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", action="store_true")
    parser.add_argument("-p", "--process", action="store_true")
    parser.add_argument("-u", "--upload", action="store_true")
    parser.add_argument("-r", "--reindex", action="store_true")
    parser.add_argument("-d", "--delete", action="store_true")
    parser.add_argument("-c", "--compact", action="store_true")
    parser.add_argument("-ms", "--maintenance_status", action="store_true")
    args = parser.parse_args()

    config = get_config()

    taxonomies_graph = CustomTaxonomiesGraph(config.taxonomies_directory)
    graph = CustomGraph(config, taxonomies_graph)

    pipeline = FairspacePipeline(config, graph)
    pipeline.run(args.init, args.process, args.upload, args.delete, args.reindex, args.compact, args.maintenance_status)


if __name__ == '__main__':
    main()
```

#### Optional implementation

If a custom processing needs to be applied, implement a custom IO handler class that extends [the `IOHandler` class](src/fairspace_pipeline/io/io_handler.py),
following examples of [the `LocalIOHandler` class](src/fairspace_pipeline/io/local_io_handler.py) and [the `S3IOHandler` class](src/fairspace_pipeline/io/s3_io_handler.py).

## Running the complete pipeline

When all the components are implemented, the pipeline can be run with the following command:

```shell
python main.py --init --process --upload --compact
```
Include only the options that you need:

- `--init` or `-i` - prepare required roles for the configured user and upload taxonomies
- `--process` or `-p` - read the input source data, transform to Fairspace model and save to the configured output directory
- `--upload` or `-u` - upload the transform data into Fairspace
- `--reindex` or `-r` - reindex Fairspace views database
- `--compact` or `-c` - compact Fairspace Jena database to reduce the size
- `--maintenance_status` or `-ms` - get the maintenance status to see if reindexing or compacting is in progress
