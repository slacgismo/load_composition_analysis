"""End-use load components
"""

import sys
import pandas as pd
from pathlib import Path

rootdir = Path(__file__).parent.parent.parent


def find_csvfile(name):
    return str(rootdir) + "/data/enduse/" + name + ".csv"


enduse_indexes = ["building_type", "component"]
residential_enduses = [
    "heating",
    "cooling",
    "computer",
    "dryer",
    "entertainment",
    "freezer",
    "hotwater",
    "lights",
    "other",
    "oven",
    "plugs",
    "refrigeration",
    "washer",
]
commercial_enduses = [
    "heating",
    "cooling",
    "ventilation",
    "hotwater",
    "cooking",
    "refrigeration",
    "exterior_lights",
    "interior_lights",
    "office_equipment",
    "miscellaneous",
    "process",
    "motors",
    "air_compressors",
]
all_enduses = list(set(residential_enduses).union(commercial_enduses))
load_components = [
    "motor_a",
    "motor_b",
    "motor_c",
    "motor_d",
    "power_electronics",
    "constant_current",
    "constant_impedance",
]


def enduse_components(
    select={},
    index=enduse_indexes,
    columns=all_enduses,
    convert=pd.DataFrame,
    version="latest",
):
    """Get enduse components data

    Enduse components provides information about how to map enduses to
    load components using "rules of association".

    Parameters:
        select (dict): specifies the row constraints (default is {})
        index (str or list): specifies rows to use as indexes (default is 'location')
        columns (str or list): specifies the columns to return (default is all columns)
        convert (callable or class): specifies the data type to return (default is DataFrame)
        version (int or str): specifies the version of the data to use (default is 'latest')

    Returns: (DataFrame or convert)
    """
    data = pd.read_csv(find_csvfile(f"components-{version}"))
    for key, value in select.items():
        data = data[data[key] == value]
    if index:
        return convert(data.set_index(index)[columns])
    else:
        return convert(data[columns])
