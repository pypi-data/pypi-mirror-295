"""
risk/annotations/io
~~~~~~~~~~~~~~~~~~~

This file contains the code for the RISK class and command-line access.
"""

import json
from typing import Any, Dict

import networkx as nx
import pandas as pd

from risk.annotations.annotations import load_annotations
from risk.log import params, print_header


class AnnotationsIO:
    """Handles the loading and exporting of annotations in various file formats.

    The AnnotationsIO class provides methods to load annotations from different file types (JSON, CSV, Excel, etc.)
    and to export parameter data to various formats like JSON, CSV, and text files.
    """

    def __init__(self):
        pass

    def load_json_annotation(self, filepath: str, network: nx.Graph) -> Dict[str, Any]:
        """Load annotations from a JSON file and convert them to a DataFrame.

        Args:
            filepath (str): Path to the JSON annotations file.
            network (NetworkX graph): The network to which the annotations are related.

        Returns:
            dict: A dictionary containing ordered nodes, ordered annotations, and the annotations matrix.
        """
        filetype = "JSON"
        params.log_annotations(filepath=filepath, filetype=filetype)
        _log_loading(filetype, filepath=filepath)
        # Open and read the JSON file
        with open(filepath, "r") as file:
            annotations_input = json.load(file)

        # Process the JSON data and return it in the context of the network
        return load_annotations(network, annotations_input)

    def load_excel_annotation(
        self,
        filepath: str,
        network: nx.Graph,
        label_colname: str = "label",
        nodes_colname: str = "nodes",
        sheet_name: str = "Sheet1",
        nodes_delimiter: str = ";",
    ) -> Dict[str, Any]:
        """Load annotations from an Excel file and associate them with the network.

        Args:
            filepath (str): Path to the Excel annotations file.
            network (nx.Graph): The NetworkX graph to which the annotations are related.
            label_colname (str): Name of the column containing the labels (e.g., GO terms).
            nodes_colname (str): Name of the column containing the nodes associated with each label.
            sheet_name (str, optional): The name of the Excel sheet to load (default is 'Sheet1').
            nodes_delimiter (str, optional): Delimiter used to separate multiple nodes within the nodes column (default is ';').

        Returns:
            Dict[str, Any]: A dictionary where each label is paired with its respective list of nodes,
                            linked to the provided network.
        """
        filetype = "Excel"
        params.log_annotations(filepath=filepath, filetype=filetype)
        _log_loading(filetype, filepath=filepath)
        # Load the specified sheet from the Excel file
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        # Split the nodes column by the specified nodes_delimiter
        df[nodes_colname] = df[nodes_colname].apply(lambda x: x.split(nodes_delimiter))
        # Convert the DataFrame to a dictionary pairing labels with their corresponding nodes
        label_node_dict = df.set_index(label_colname)[nodes_colname].to_dict()
        return load_annotations(network, label_node_dict)

    def load_csv_annotation(
        self,
        filepath: str,
        network: nx.Graph,
        label_colname: str = "label",
        nodes_colname: str = "nodes",
        nodes_delimiter: str = ";",
    ) -> Dict[str, Any]:
        """Load annotations from a CSV file and associate them with the network.

        Args:
            filepath (str): Path to the CSV annotations file.
            network (nx.Graph): The NetworkX graph to which the annotations are related.
            label_colname (str): Name of the column containing the labels (e.g., GO terms).
            nodes_colname (str): Name of the column containing the nodes associated with each label.
            nodes_delimiter (str, optional): Delimiter used to separate multiple nodes within the nodes column (default is ';').

        Returns:
            Dict[str, Any]: A dictionary where each label is paired with its respective list of nodes,
                            linked to the provided network.
        """
        filetype = "CSV"
        params.log_annotations(filepath=filepath, filetype=filetype)
        _log_loading(filetype, filepath=filepath)
        # Load the CSV file into a dictionary
        annotations_input = _load_matrix_file(
            filepath, label_colname, nodes_colname, delimiter=",", nodes_delimiter=nodes_delimiter
        )
        # Process and return the annotations in the context of the network
        return load_annotations(network, annotations_input)

    def load_tsv_annotation(
        self,
        filepath: str,
        network: nx.Graph,
        label_colname: str = "label",
        nodes_colname: str = "nodes",
        nodes_delimiter: str = ";",
    ) -> Dict[str, Any]:
        """Load annotations from a TSV file and associate them with the network.

        Args:
            filepath (str): Path to the TSV annotations file.
            network (nx.Graph): The NetworkX graph to which the annotations are related.
            label_colname (str): Name of the column containing the labels (e.g., GO terms).
            nodes_colname (str): Name of the column containing the nodes associated with each label.
            nodes_delimiter (str, optional): Delimiter used to separate multiple nodes within the nodes column (default is ';').

        Returns:
            Dict[str, Any]: A dictionary where each label is paired with its respective list of nodes,
                            linked to the provided network.
        """
        filetype = "TSV"
        params.log_annotations(filepath=filepath, filetype=filetype)
        _log_loading(filetype, filepath=filepath)
        # Load the TSV file into a dictionary
        annotations_input = _load_matrix_file(
            filepath, label_colname, nodes_colname, delimiter="\t", nodes_delimiter=nodes_delimiter
        )
        # Process and return the annotations in the context of the network
        return load_annotations(network, annotations_input)


def _load_matrix_file(
    filepath: str,
    label_colname: str,
    nodes_colname: str,
    delimiter: str = ",",
    nodes_delimiter: str = ";",
) -> Dict[str, Any]:
    """Load annotations from a CSV or TSV file and convert them to a dictionary.

    Args:
        filepath (str): Path to the annotation file.
        label_colname (str): Name of the column containing the labels (e.g., GO terms).
        nodes_colname (str): Name of the column containing the nodes associated with each label.
        delimiter (str, optional): Delimiter used to separate columns in the file (default is ',').
        nodes_delimiter (str, optional): Delimiter used to separate multiple nodes within the nodes column (default is ';').

    Returns:
        Dict[str, Any]: A dictionary where each label is paired with its respective list of nodes.
    """
    # Load the CSV or TSV file into a DataFrame
    df = pd.read_csv(filepath, delimiter=delimiter)
    # Split the nodes column by the nodes_delimiter to handle multiple nodes per label
    df[nodes_colname] = df[nodes_colname].apply(lambda x: x.split(nodes_delimiter))
    # Create a dictionary pairing labels with their corresponding list of nodes
    label_node_dict = df.set_index(label_colname)[nodes_colname].to_dict()
    return label_node_dict


def _log_loading(filetype: str, filepath: str = "") -> None:
    """Log information about the network file being loaded.

    Args:
        filetype (str): The type of the file being loaded (e.g., 'Cytoscape').
        filepath (str, optional): The path to the file being loaded.
    """
    print_header("Loading annotations")
    print(f"Filetype: {filetype}")
    if filepath:
        print(f"Filepath: {filepath}")
