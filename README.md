Download-Transform-Merge Template
================================================
KG-Hub template for tools to generate knowledge graphs for projects

Documentation
------------------------------------------------

This template could be used for data ingestion for varied sources.

**Components**

- Download: The [download.yaml](download.yaml) contains all the URLs for the source data.
- Transform: The [transform_utils](project_name/transform_utils) contains the code relevant to trnsformations of the raw data into nodes and edges (tsv format)
- Merge: Implementation of the 'merge' function from [KGX](https://github.com/biolink/kgx) using [merge.yaml](merge.yaml) as a source file.

**Utilities**

The code for these are found in the [utils](project_name/utils) folder.

- [ROBOT](https://github.com/ontodev/robot) for transforming ontology.OWL to ontology.JSON

**Examples Included**

Thes examples have download links and transform codes from other projects.

- Ontology: Sampled from [kg-covid-19](https://github.com/Knowledge-Graph-Hub/kg-covid-19). Code located [here](project_name/transform_utils/ontology)
- Example Transform: Sampled from [kg-covid-19](https://github.com/Knowledge-Graph-Hub/kg-covid-19). Code located [here](project_name/transform_utils/drug_central).

The [merge.yaml](merge.yaml) shows merging of the various KGs. In this example we have ENVO, CHEBI, NCBITaxon and the Traits KGs merged.

**Usage**

[Use this template](https://github.com/Knowledge-Graph-Hub/kg-dtm-template/generate) to generate a template in the desired repository and then refactor the string `project_name` in the project to the desired project name. 

*Running in a container*: the Dockerfile in this directory will set up a Docker container for running the code in this repository. This may help if you experience any issues running the template in your software environment (e.g., if you're using Windows or can't update your Python version). Ensure Docker is installed, then from your own clone of this repository, run the following:

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
