import airtable
import pandas as pd
import numpy as np
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

    def __init__(self, base_id, table_name, fields = [], **kwargs):
        self.table_name = table_name
        self.base_id = base_id
        self.fields = fields

        self.df = self.dict_to_df(self.base_id, self.table_name,fields)
        display(self.df)
        
    

    def dict_to_df(self, base_id : str, table_name : str, fields : list):
        at = airtable.Airtable(base_id, READ_ACCESS_TOKEN)
        
        f = at.iterate(table_name, batch_size=0, filter_by_formula=None,
                       view=None, max_records=0, fields=fields)
        result = { "records": [] }
        for r in f:
            result["records"].append(r)

        results = { "records": [] }
        for r in result['records']:
            results["records"].append(r['fields'])
        return pd.DataFrame(results['records'])
    


class FlyDataTable(Table):
    """
    Class for FlyDataTable
    """
    def __init__(self, table_name, fields, **kwargs):
        super().__init__(FLYDATA_BASE_ID,table_name, fields, **kwargs)


class TwoPhotonRecordingTable(FlyDataTable):
    """
    Class for TwoPhotonRecordingTable
    """
    def __init__(self, **kwargs):

        self.fields = ['recording_id', 'recording_file_id',
                        'recording_type', 'recording_solution', 
                        'recording_time', 'completed', 'tags', 
                        'dict', 'comments', 'neuron_section', 
                        'brain_area','linescan', 'subject_id (from subject_id)']
        
        super().__init__(table_name='TwoPhotonRecording', fields = self.fields, **kwargs)

        self.df = self.format_df()

    def format_df(self):
        temp =self.df.rename(columns={'subject_id (from subject_id)' : 'subject_id'})
        temp['subject_id'] = [i[0] for i in temp['subject_id']]
        cols = temp.columns[:-1]
        return temp[cols.insert(0,['subject_id'])]




class FlySubjectTable(FlyDataTable):
    """
    Class for TwoPhotonRecordingTable
    """
    def __init__(self, **kwargs):
        
        self.fields = ['subject_id','genotype_id',
                       'subject_name','experimenter',
                       'rearing_method','sex','age',
                       'prep_time']
        
        super().__init__(table_name='FlySubject', fields = self.fields, **kwargs)