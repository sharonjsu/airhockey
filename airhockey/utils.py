from airtable import Airtable
import pandas as pd
from pandas import DataFrame
from typing import Any

def link_id_fetch(at : Airtable, table_name: str,  id : str, field : str) -> Any: 
    """
    Gets field value for a particular record ID

    Parameters
    ----------
    at : Airtable object

    table_name : str
        Name of table containing record_id
    
    id : str
        record_id to search for
    
    field : str
        Field to obtain return value from

    """
    return at.get(table_name, record_id = id)['fields'][field]


def itr_to_df(f : Airtable)-> DataFrame:
    """
    Converts Airtable.iterator to a pandas DataFrame object.
    
    Parameters
    ----------
    f : Airtable.generator
        Created using Airtable.iterator() call
    """
    result = { "records": [] }
    for r in f:
        result["records"].append(r)
    results = { "records": [] }
    for r in result['records']:
        results["records"].append(r['fields'])
    return pd.DataFrame(results['records'])