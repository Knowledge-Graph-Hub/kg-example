# KG-Hub Download-Transform-Merge Template

KG-Hub repository template for new knowledge graph projects.

## Documentation

This template repository contains every component necessary to get started with building a new knowledge graph compatible with KG-Hub. It may be used for data ingestion for varied sources, transformation from various data formats to graph node/edge files, and merge functions.

### Components

- Download: The [download.yaml](download.yaml) contains all the URLs for the source data.
- Transform: The [transform_utils](project_name/transform_utils) contains the code relevant to trnsformations of the raw data into nodes and edges (tsv format)
- Merge: Implementation of the 'merge' function from [KGX](https://github.com/biolink/kgx) using [merge.yaml](merge.yaml) as a source file.

An alternative merge option based on [cat-merge](https://github.com/monarch-initiative/cat-merge) is also included. This approach may be appropriate for graphs with many different sources, though it does much less than the standard KGX-driven method to account for duplicated or similar nodes.

### Usage

[Use this template](https://github.com/Knowledge-Graph-Hub/kg-template/generate) to generate a template in the desired repository and then refactor the string `project_name` in the project to the desired project name.

Install with `pip`:

```
python -m pip install .
```

To download sources:

```
python run.py download
```

By default, this will read from `download.yaml` and save downloaded data to `data/raw`.

To transform downloaded sources:

```
python run.py transform
```

By default, this will run all transforms defined in `transform.py` and save results to `data/transformed`.  Use the `-s` option with a transform name to run just one, e.g., `python run.py transform -s EnvoTransform`.

To build the merged graph:

```
python run.py merge
```

By default, this will merge all inputs defined in `merge.py` and save results to `data/merged`.

Alternatively, run cat-merge:

```
python run.py catmerge
```

By default, this will merge all inputs in `data/transformed` and save results to `data/merged`. It also generates reports which you can find in `data/merged/qc_report.yaml` and `data/merged/qc` once the merge completes.

#### Running in a container

The Dockerfile in this directory will set up a Docker container for running the code in this repository. This may help if you experience any issues running the template in your software environment (e.g., if you're using Windows or can't update your Python version). Ensure Docker is installed, then from your own clone of this repository, run the following:

```
docker build -t "kg-dtm:Dockerfile" .
```

You should then see the new image when you run

```
docker images
```

Then enter it with the following command and continue on your KG assembly journey.

```
docker run -it kg-dtm bash
```

### Utilities

The code for these are found in the [utils](project_name/utils) folder.

- [ROBOT](https://github.com/ontodev/robot) for transforming ontology.OWL to ontology.JSON. Functions for working with ROBOT are in `robot_utils.py`.

- Transformation utilities. The functions in `transform_utils.py` may be helpful when completing data transforms. For example, to remove obsolete nodes and the related edges from a source or even from a merged graph, use the following code, changing `project_name` and paths as needed:

```
from project_name.utils.transform_utils import remove_obsoletes
remove_obsoletes("data/transformed/source/nodes.tsv","data/transformed/source/edges.tsv")
```

### Examples

These examples are sampled from [kg-covid-19](https://github.com/Knowledge-Graph-Hub/kg-covid-19).

- Ontology: Code located [here](project_name/transform_utils/ontology).

- Example Transform: Code located [here](project_name/transform_utils/drug_central).

The [merge.yaml](merge.yaml) shows merging of the various graphs. In this example we have ENVO, CHEBI, and Reactome pathways.
