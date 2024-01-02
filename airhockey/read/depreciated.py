from airhockey.read.table import GenotypeTables
from IPython.display import display

class Stocks(GenotypeTables):
    """
    Class for Stocks
    """

    def __init__(self,**kwargs):
        self.fields = ['stock_id', 'genotype_id', 'status', 'fly_origin', 
       'experimenter', 'chr1 (from FlyGenotype)', 'chr2 (from FlyGenotype)',
       'chr3 (from FlyGenotype)', 'chr4 (from FlyGenotype)',
       'public_ids (from FlyGenotype)','tags (from FlyGenotype)',
        'comments (from FlyGenotype)', 'Last modified']

        # To Do: write function that parses kwargs being sent in here and passes the new correct title kwargs lmao
        col_dict = {'chr1 (from FlyGenotype)' : 'chr1', 
                        'chr2 (from FlyGenotype)' : 'chr2',
                        'chr3 (from FlyGenotype)' : 'chr3', 
                        'chr4 (from FlyGenotype)' : 'chr4',
                        'public_ids (from FlyGenotype)' : 'public_ids',
                        'tags (from FlyGenotype)' : 'tags',
                        'comments (from FlyGenotype)' : 'comments'}
        self.inv_col = {v: k for k, v in col_dict.items()}
 
        n_kwargs = self.kwarg_converter(kwargs)
        


        super().__init__(table_name = 'Stocks', fields = self.fields, **n_kwargs)

        # self.format_df()

        display(self.df)

    def format_df(self):
        col_dict = {'chr1 (from FlyGenotype)' : 'chr1', 
                                'chr2 (from FlyGenotype)' : 'chr2',
                                'chr3 (from FlyGenotype)' : 'chr3', 
                                'chr4 (from FlyGenotype)' : 'chr4',
                                'public_ids (from FlyGenotype)' : 'public_ids',
                                'tags (from FlyGenotype)' : 'tags',
                                'comments (from FlyGenotype)' : 'comments'}

        self.df = self.df.rename(columns = col_dict)
        for value in col_dict.values():
            self.df[value] = [i[0] for i in self.df[value]]
        cols = ['stock_id', 'genotype_id', 'chr1', 'chr2', 'chr3', 'chr4',
                'status', 'fly_origin', 'experimenter',
                'public_ids', 'tags', 'comments', 'Last modified']

        self.df = self.df[cols]

        return
    
    def kwarg_converter(self,kwargs):
        new_kwargs={}
        for oldkey, value in kwargs.items():
            new_kwargs[self.inv_col[oldkey]] = kwargs.get(oldkey)
        print(new_kwargs)
        return new_kwargs