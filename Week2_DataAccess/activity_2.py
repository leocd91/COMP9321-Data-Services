import sqlite3
import pandas as pd
from pandas.io import sql
import os

def read_csv(csv_file):
    """
    :param csv_file: the path of csv file
    :return: A dataframe out of the csv file
    """
    return pd.read_csv(csv_file)


def write_in_sqlite(dataframe, database_file, table_name):
    """
    :param dataframe: The dataframe which must be written into the database
    :param database_file: where the database is stored
    :param table_name: the name of the table
    """

    cnx = sqlite3.connect(database_file)
    sql.to_sql(dataframe, name=table_name, con=cnx)


def read_from_sqlite(database_file, table_name, index_col=None):
    """
    :param database_file: where the database is stored
    :param table_name: the name of the table
    :param index_col (optional): name of columns in db as index
    :return: A Dataframe
    """
    cnx = sqlite3.connect(database_file)
    return sql.read_sql('select * from ' + table_name, cnx, index_col=index_col)


if __name__ == '__main__':
    table_name = "Demographic_Statistics"
    database_file = 'Demographic_Statistics.db'  # name of sqlite db file that will be created
    csv_file = 'Demographic_Statistics_By_Zip_Code.csv'  # path to the downloaded csv file
    loaded_df = read_csv(csv_file)

    print("Creating database")
    if os.path.exists(database_file):
        print(database_file + "already exists.")
    else:
        write_in_sqlite(loaded_df, database_file, table_name)
        
    print("Querying the database")
    queried_df = read_from_sqlite(database_file, table_name, index_col='index')

    pd.set_option('display.width', 1000)
    pd.options.display.max_colwidth = 3
    pd.set_option('display.max_columns', 7)

    print(queried_df.head(10))
