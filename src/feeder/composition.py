"""Feeder composition
"""

import pandas as pd
from pathlib import Path

rootdir = Path(__file__).parent.parent.parent

feeder_component_indexes = ["region", "feeder_type", "building_type"]
feeder_component_data = [
    "floorarea_per_building",
    "number_of_buildings",
    "floorarea",
    "composition",
]


def feeder_composition(
    select={},
    index=feeder_component_indexes,
    columns=feeder_component_data,
    convert=pd.DataFrame,
    version="latest",
):
    """Get feeder composition data

    Feeder composition provides information about different economic activites
    taking place of different types of feeder.

    Parameters:
        select (dict): specifies the row constraints (default is {})
        index (str or list): specifies rows to use as indexes (default is 'location')
        columns (str or list): specifies the columns to return (default is all columns)
        convert (callable or class): specifies the data type to return (default is DataFrame)
        version (int or str): specifies the version of the data to use (default is 'latest')

    Returns: (DataFrame or convert)
    """
    data = pd.read_csv(str(rootdir) + f"/data/feeder/composition-{version}.csv")
    for key, value in select.items():
        data = data[data[key] == value]
    data["floorarea"] = data["floorarea_per_building"] * data["number_of_buildings"]
    data["composition"] = data["floorarea"] / sum(data["floorarea"])
    if index:
        return convert(data.set_index(index)[columns])
    else:
        return convert(data[columns])
