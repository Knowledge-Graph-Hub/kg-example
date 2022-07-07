#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import click
from project_name import download as kg_download
from project_name import transform as kg_transform
from project_name.merge_utils.merge_kg import load_and_merge, merge_with_cat_merge
from project_name.transform import DATA_SOURCES


@click.group()
def cli():
    pass


@cli.command()
@click.option("yaml_file", "-y", required=True, default="download.yaml",
              type=click.Path(exists=True))
@click.option("output_dir", "-o", required=True, default="data/raw")
@click.option("snippet_only", "-x", is_flag=True, default=False,
              help='Download only the first 5 kB of each (uncompressed) source, for testing and file checks [false]')
@click.option("ignore_cache", "-i", is_flag=True, default=False,
              help='ignore cache and download files even if they exist [false]')
def download(*args, **kwargs) -> None:
    """Downloads data files from list of URLs (default: download.yaml) into data
    directory (default: data/raw).

    Args:
        yaml_file: Specify the YAML file containing a list of datasets to download.
        output_dir: A string pointing to the directory to download data to.
        snippet_only: Downloads only the first 5 kB of the source, for testing and file checks.  
        ignore_cache: If specified, will ignore existing files and download again.

    Returns:
        None.

    """

    kg_download(*args, **kwargs)

    return None


@cli.command()
@click.option("input_dir", "-i", default="data/raw", type=click.Path(exists=True))
@click.option("output_dir", "-o", default="data/transformed")
@click.option("sources", "-s", default=None, multiple=True,
              type=click.Choice(DATA_SOURCES.keys()))
def transform(*args, **kwargs) -> None:
    """Calls scripts in project_name/transform/[source name]/ to transform each source
    into nodes and edges.

    Args:
        input_dir: A string pointing to the directory to import data from.
        output_dir: A string pointing to the directory to output data to.
        sources: A list of sources to transform.

    Returns:
        None.

    """

    # call transform script for each source
    kg_transform(*args, **kwargs)

    return None


@cli.command()
@click.option('yaml', '-y', default="merge.yaml", type=click.Path(exists=True))
@click.option('processes', '-p', default=1, type=int)
def merge(yaml: str, processes: int) -> None:
    """Use KGX to load subgraphs to create a merged graph.

    Args:
        yaml: A string pointing to a KGX compatible config YAML.
        processes: Number of processes to use.

    Returns:
        None.

    """

    load_and_merge(yaml, processes)

@cli.command()
@click.option("--merge_all",
                is_flag=True,
                help="""Include *all* transformed sources.""")
@click.option("--include_only",
                callback=lambda _,__,x: x.split(',') if x else [],
                help="""One or more transformed sources to merge, and only these,
                     comma-delimited and named by their directory name, e.g., reactome.""")
@click.option("--exclude",
                callback=lambda _,__,x: x.split(',') if x else [],
                help="""One or more transformed sources to exclude from merging,
                     comma-delimited and named by their directory name, e.g., reactome.
                     Will select all other transformed sources for merging.""")
def catmerge(merge_all=False, include_only=[], exclude=[]) -> None:
    """Use cat-merge to create a merged graph.
    Args:
        merge_all: Include *all* transformed sources.
        include_only: Include only the specified transformed sources.
        exclude: Include all transformed sources *except* those specified.
    Returns:
        None.
    """

    merge_with_cat_merge(merge_all, include_only, exclude)

if __name__ == "__main__":
    cli()
