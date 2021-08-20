"""Load electrification
"""

import sys
import pandas as pd
from pathlib import Path

rootdir = Path(__file__).parent.parent.parent


def find_csvfile(name):
    return str(rootdir) + f"/data/electrification/{name}.csv"


electrification_index = ["location"]
electrification_data = [
    "heat_pump",
    "other_electric_heat",
    "cooling",
    "water_heating",
    "cooking",
]
electrification_attributes = ["city", "region", "building_type"]


def load_electrification(
    select={},
    index="location",
    columns=[
        "city",
        "region",
        "building_type",
        "heat_pump",
        "other_electric_heat",
        "cooling",
        "water_heating",
        "cooking",
    ],
    convert=pd.DataFrame,
    version="latest",
):
    """Get load electrification data

    Load electrification provides information about what fraction of specified
    enduses are electric.

    Parameters:
        select (dict): specifies the row constraints (default is {})
        index (str or list): specifies rows to use as indexes (default is 'location')
        columns (str or list): specifies the columns to return (default is all columns)
        convert (callable or class): specifies the data type to return (default is DataFrame)
        version (int or str): specifies the version of the data to use (default is 'latest')

    Returns: (DataFrame or convert)
    """
    data = pd.read_csv(find_csvfile(f"loads-{version}"))
    for key, value in select.items():
        data = data[data[key] == value]
    return convert(data.set_index(index)[columns])
