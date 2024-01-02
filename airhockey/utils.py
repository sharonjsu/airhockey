import airtable
from typing import Any

def link_id_fetch(at : airtable, table_name: str,  id : str, field : str) -> Any: 
    return at.get(table_name, record_id = id)['fields'][field]
