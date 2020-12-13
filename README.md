DTM-Template
================================================
KG hub to produce a knowledge graph for projects

Documentation
------------------------------------------------

This template could be used for data ingestion for varied sources. The name stands for **D** ownload - **T** ransform - **M** erge template.

**Components**

- Download: The `download.yaml` contains all the URLs for the source data.
- Transform: The [transform_utils](project_name/transform_utils) contains the code relevant to trnsformations of the raw data into nodes and edges (tsv format)
- Merge: Implementation of the 'merge' function from [KGX](https://github.com/biolink/kgx)

**Utilities**

- NLP using [OGER](https://github.com/OntoGene/OGER)
- [ROBOT](https://github.com/ontodev/robot) for transforming OWL to JSON
