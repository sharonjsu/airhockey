import airtable
import pandas as pd
from IPython.display import display
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


class TwoPhotonRecording(FlyDataTable):
    """
    Class for TwoPhotonRecording

    Note 1 : Query by subject_id alone is slower and separate from other
    classes due airtable naming scheme.
    To speed things up, query by a set of recording IDs instead.
    s
    Note 2 : If "recording_file_id" == -1, that means you did not write down
    the recording_file_id. Please go edit that in airtable.

    Parameters
    ----------
    subject_id : int or List[int]


    """
    def __init__(self, **kwargs):

        self.fields = ['recording_id', 'recording_file_id', 'recording_type', 
                       'recording_solution', 'recording_time', 'completed', 
                       'tags', 'dict', 'comments', 'neuron_section',
                       'brain_area', 'linescan', 'subject_id (from subject_id)'
                       ]
        
        if kwargs.get('subject_id') is not None:
            self.subject_id = kwargs.pop('subject_id')
        else:
            self.subject_id = None

        super().__init__(table_name='TwoPhotonRecording', fields=self.fields,
                         **kwargs)

        self.__format_df()
        
        if self.subject_id is not None:
            self.__fetch_subject()

        display(self.df)

    def __format_df(self):
        self.df = self.df.rename(
            columns={'subject_id (from subject_id)': 'subject_id'})
        self.df['subject_id'] = [i[0] for i in self.df['subject_id']]
        cols = self.df.columns[:-1]
        self.df = self.df[cols.insert(0,['subject_id'])]
        self.df['recording_file_id'] = self.df['recording_file_id'].fillna(-1).astype(int)
        return

    def __fetch_subject(self):
        if isinstance(self.subject_id, int):
            self.subject_id = [self.subject_id]
        self.df = self.df[self.df['subject_id'].isin(self.subject_id)]
        return


class FlySubject(FlyDataTable):
    """
    Class for FlySubject
    """
    def __init__(self, **kwargs):
        self.fields = ['subject_id', 'genotype_id',
                       'subject_name', 'experimenter',
                       'rearing_method', 'sex', 'age',
                       'prep_time']
        self.formula = "NOT({genotype_id} = '')"

        super().__init__(table_name='FlySubject', fields=self.fields,
                         formula=self.formula, **kwargs)

        display(self.df)


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


class FlyGenotype(GenotypeTables):
    """
    Class for FlyGenotype. 
    Querying for genotypes does not have to be exact.
    """

    def __init__(self, **kwargs):
        super().__init__(table_name='FlyGenotype', **kwargs)
        display(self.df)


class Stocks(GenotypeTables):
    """
    Class for Stocks
    """

    def __init__(self, **kwargs):
        self.fields = ['stock_id', 'genotype_id']
        super().__init__(table_name='Stocks', fields=self.fields, **kwargs)

        display(self.df)
