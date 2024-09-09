import pathlib

import pandas as pd
from .. import BaseDataset
from ..db_utils import create_connection

HERE = pathlib.Path(__file__).resolve().parent


class DDIMDLDataset(BaseDataset):
    def __init__(self,  chemical_property_columns=['enzyme',
                                                   'target',
                                                   'pathway',
                                                   'smile'],
                 embedding_columns=[],
                 ner_columns=[],
                 **kwargs):

        super().__init__(chemical_property_columns, embedding_columns,
                         ner_columns, **kwargs)

        # kwargs = {'index_path': str(HERE.joinpath('indexes'))}
        kwargs['index_path']= str(HERE.joinpath('indexes'))

        db = HERE.joinpath('event.db')
        conn = create_connection(db)
        print("db prep")
        self.drugs_df = self.__select_all_drugs_as_dataframe__(conn)
        self.ddis_df = self.__select_all_events__(conn)
        print("db bitti")
        self.index_path = kwargs.get('index_path')

    def __select_all_drugs_as_dataframe__(self, conn):
        headers = ['index', 'id', 'name',
                   'target', 'enzyme', 'pathway', 'smile']
        cur = conn.cursor()
        cur.execute(
            '''select "index", id, name, target, enzyme, pathway, smile from drug''')
        rows = cur.fetchall()
        df = pd.DataFrame(columns=headers, data=rows)
        df['enzyme'] = df['enzyme'].apply(lambda x: x.split('|'))
        df['target'] = df['target'].apply(lambda x: x.split('|'))
        df['pathway'] = df['pathway'].apply(lambda x: x.split('|'))
        df['smile'] = df['smile'].apply(lambda x: x.split('|'))
        return df

    def __select_all_events__(self, conn):
        """
        Query all rows in the event table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute('''
                select ex."index", d1.id, d1.name, d2.id, d2.name,  mechanism || ' ' ||action from extraction ex
                join drug d1 on  d1.name = ex.drugA
                join drug d2 on  d2.name = ex.drugB
        ''')

        rows = cur.fetchall()

        headers = ["index", "id1", "name1", "id2", "name2", "event_category"]
        return pd.DataFrame(columns=headers, data=rows)
