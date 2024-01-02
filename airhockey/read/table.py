import airtable
import pandas as pd
from airhockey.config import READ_ACCESS_TOKEN
from airhockey.config import FLYDATA_BASE_ID

class Table:
    """
    Parent class for table parsing

    Parameters
    ----------
    BASE_ID : str

    table_name : str
    
    """

    def __init__(self, base_id, table_name, **kwargs):
        self.at = airtable.Airtable(base_id, READ_ACCESS_TOKEN)
        self.table_name = table_name
        self.fields = kwargs.pop('fields', None)

        if kwargs:
            self.formula = self.format_formula(kwargs)
        else:
            self.formula = None
        
        self.df = self.dict_to_df()

    def dict_to_df(self):
        f = self.at.iterate(self.table_name, batch_size=0,
                            filter_by_formula=self.formula,
                            view=None, max_records=0, fields=self.fields)
        result = {"records": []}
        for r in f:
            result["records"].append(r)

        results = {"records": []}
        for r in result['records']:
            results["records"].append(r['fields'])
        return pd.DataFrame(results['records'])
   
    def format_formula(self, kwargs: dict):
        if kwargs.get('formula'):
            temp = f"{kwargs.pop('formula')}, "
        else:
            temp = ""

        for key, value in kwargs.items():
            if value is list:
                temp += self.list_parse(key, value)+", "
            elif value is str:
                temp += "{%s} = " % key + f"'{value}', "
            else:
                temp += "{%s} = " % key + f"{value}, "
        return f"AND({temp[:-2]})"

    def list_parse(self, key, value):
        temp = ""
        for i in value:
            temp += "{%s} = " % key + f"{i}, "
        
        return f"OR({temp[:-2]})"


class FlyDataTable(Table):
    """
    Parent Class for FlyDataTable
    """
    def __init__(self, table_name, **kwargs):
        super().__init__(FLYDATA_BASE_ID, table_name, **kwargs)


class GenotypeTables(FlyDataTable):
    """
    Parent class for Genotype Tables where FIND() is implemented. 
    Querying for genotypes does not have to be exact.
    """
    def __init__(self, table_name, **kwargs):
        self.fields = kwargs.pop('fields',None)

        if kwargs:
            super().__init__(table_name, fields=self.fields, 
                             formula=self.find_format_formula(kwargs))
        else:
            super().__init__(table_name, fields=self.fields)

    def find_format_formula(self, kwargs: dict):
        if kwargs.get('formula'):
            temp = f"{kwargs.pop('formula')}, "
        else:
            temp = ""

        for key, value in kwargs.items():
            if value is list:
                temp += self.soft_list_parse(key, value)+", "
            else:
                temp += f"FIND('{value}'," + "{%s}), " % key
        return temp[:-2]

    def soft_list_parse(self, key, value):
        temp = ""
        for i in value:
            temp += f"FIND('{value}'," + "{%s})" % key
        return f"OR({temp[:-2]})"