from typing import Dict, List
import os
import yaml
import networkx as nx
from kgx.cli.cli_utils import merge

import pandas as pd

from cat_merge.merge import merge as cat_merge_merge # type: ignore

INPUT_DATA_PATH = "data/transformed/"

def parse_load_config(yaml_file: str) -> Dict:
    """Parse load config YAML.

    Args:
        yaml_file: A string pointing to a KGX compatible config YAML.

    Returns:
        Dict: The config as a dictionary.

    """
    with open(yaml_file) as YML:
        config = yaml.load(YML, Loader=yaml.FullLoader)
    return config


def load_and_merge(yaml_file: str, processes: int = 1) -> nx.MultiDiGraph:
    """Load and merge sources defined in the config YAML.

    Args:
        yaml_file: A string pointing to a KGX compatible config YAML.
        processes: Number of processes to use.

    Returns:
        networkx.MultiDiGraph: The merged graph.

    """
    merged_graph = merge(yaml_file, processes=processes)
    return merged_graph

def merge_with_cat_merge(merge_all: bool, include_only: list, exclude: list) -> None:
    """Load and merge sources with cat-merge.

    Args:
        merge_all: if True, merge all ontology node and edges.
        include_only: list of paths to ontology node/edgefiles to include
        exclude: list of paths to ontology node/edgefiles to exclude

    Returns:
        None

    """
    
    nodepaths = []
    edgepaths = []

    # Need to know input names and filepaths
    # Keys in input_paths are transform names, values are lists of filepaths
    input_paths = {}
    if len(include_only) > 0:
        input_dirs = [dirname for dirname in os.listdir(INPUT_DATA_PATH) if \
            os.path.isdir(os.path.join(INPUT_DATA_PATH, dirname)) and dirname in include_only]
    elif len(exclude) > 0:
        input_dirs = [dirname for dirname in os.listdir(INPUT_DATA_PATH) if \
            os.path.isdir(os.path.join(INPUT_DATA_PATH, dirname)) and dirname not in exclude]
    else:
        input_dirs = [dirname for dirname in os.listdir(INPUT_DATA_PATH) if \
            os.path.isdir(os.path.join(INPUT_DATA_PATH, dirname))]
    for dirname in input_dirs:
        this_path = os.path.join(INPUT_DATA_PATH,dirname)
        input_paths[dirname] = [os.path.join(this_path, filename) for filename in \
            os.listdir(this_path) if os.path.isfile(os.path.join(this_path, filename)) and filename.endswith(".tsv")]

    # Separate out nodelists vs. edgelists
    # Do a check to verify that none of the files are empty, or the merge will fail
    # also verify the header in each contains an 'id' field
    ignore_paths = []
    for input_name in input_paths:
        print(f"Validating {input_name}...")
        for path in input_paths[input_name]:
            if path.endswith("_nodes.tsv"):
                this_edgepath = (path.rpartition('_'))[0] + '_edges.tsv'
                try:
                    nodedf = pd.read_csv(path, sep='\t', index_col='id')
                except (KeyError, TypeError, pd.errors.ParserError, pd.errors.EmptyDataError) as e:
                    ignore_paths.append(this_edgepath)
                    print(f"Ignoring {path} due to pandas parsing error. Will also ignore {this_edgepath}. Error: {e}")
                    continue
                num_lines = len(nodedf.index)
                if num_lines > 1 and path not in ignore_paths:
                    nodepaths.append(path)
                else:
                    ignore_paths.append(this_edgepath)
                    print(f"Ignoring {path} as it contains no nodes or node ids. Will also ignore {this_edgepath}.")
            elif path.endswith("_edges.tsv"):
                this_nodepath = (path.rpartition('_'))[0] + '_nodes.tsv'
                try:
                    edgedf = pd.read_csv(path, sep='\t', index_col='id')
                except (KeyError, TypeError, pd.errors.ParserError, pd.errors.EmptyDataError) as e:
                    ignore_paths.append(this_nodepath)
                    print(f"Ignoring {path} due to pandas parsing error. Will also ignore {this_nodepath}. Error: {e}")
                    continue
                num_lines = len(edgedf.index)
                if num_lines > 1 and path not in ignore_paths:
                    edgepaths.append(path)
                else:
                    ignore_paths.append(this_nodepath)
                    print(f"Ignoring {path} as it contains no edges or edge ids. Will also ignore {this_nodepath}.")

    # Default behavior is to merge all for now, but this could do something different later
    if merge_all:
        pass

    cat_merge_merge(
        name='merged-kg',
        nodes=nodepaths,
        edges=edgepaths,
        output_dir='data/merged'
    )
