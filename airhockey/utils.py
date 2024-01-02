from airtable import Airtable
import pandas as pd
from pandas import DataFrame
from typing import Any

def link_id_fetch(at : Airtable, table_name: str,  id : str, field : str) -> Any: 
    return at.get(table_name, record_id = id)['fields'][field]


def itr_to_df(f : Airtable)-> DataFrame:
    result = { "records": [] }
    for r in f:
        result["records"].append(r)
    results = { "records": [] }
    for r in result['records']:
        results["records"].append(r['fields'])
    return pd.DataFrame(results['records'])