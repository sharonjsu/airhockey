from IPython.display import display
from airhockey.read.table import FlyDataTable, GenotypeTables

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



class FlyGenotype(GenotypeTables):
    """
    Class for FlyGenotype. 
    Querying for genotypes does not have to be exact.
    """

    def __init__(self, **kwargs):
        super().__init__(table_name='FlyGenotype', **kwargs)
        display(self.df)


class Stocks(FlyDataTable):
    """
    Class for Stocks
    """

    def __init__(self, **kwargs):
        self.fields = ['stock_id', 'genotype_id']
        super().__init__(table_name='Stocks', fields=self.fields, **kwargs)

        display(self.df)

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
            kwargs['subject_id (from subject_id)'] = kwargs.pop('subject_id')
            print(kwargs)
        else:
            self.subject_id = None

        super().__init__(table_name='TwoPhotonRecording', fields=self.fields,
                         **kwargs)

        self.__format_df()
        


        display(self.df)

    def __format_df(self):
        self.df = self.df.rename(
            columns={'subject_id (from subject_id)': 'subject_id'})
        self.df['subject_id'] = [i[0] for i in self.df['subject_id']]
        cols = self.df.columns[:-1]
        self.df = self.df[cols.insert(0,['subject_id'])]
        self.df['recording_file_id'] = self.df['recording_file_id'].fillna(-1).astype(int)
        return
