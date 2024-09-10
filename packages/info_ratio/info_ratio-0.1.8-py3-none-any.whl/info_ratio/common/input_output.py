import sqlite3
import pandas as pd
from info_ratio.common.logging import loga


@loga.errors
def dfs_tabs(df_list, sheet_list, file_name):
    writer = pd.ExcelWriter(file_name, engine='openpyxl')
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, header=True,
                           startrow=0, startcol=0, index=False)
    writer.close()


@loga
def get_data(self, insert_data=False):
    with sqlite3.connect(self.db_path) as db:
        if insert_data:
            # Define the path to the Excel file
            file_uploads = [self.data_insert_path+"Holdings Historical 360 to DSP.xlsx",
                            self.data_insert_path+"Holdings Historical Edelweiss to Invesco.xlsx",
                            self.data_insert_path+"Holdings Historical ITI to PPFAS.xlsx",
                            self.data_insert_path+"Holdings Historical Quant to Zerodha.xlsx"]

            # Loop through each Excel file in 'file_uploads'
            for i in file_uploads:
                dfs = pd.read_excel(i, engine="openpyxl", skiprows=4)
                dfs.to_sql('df_table', con=db, if_exists='append')

            cols = ['CD_ISIN No', 'Bmonth_Month End', 'Bmonth_Close']
            col_rename = {'CD_ISIN No': 'Company ISIN',
                          'Bmonth_Month End': 'Numeric Date', 'Bmonth_Close': 'Price'}
            company_data_df = pd.read_excel(
                self.data_insert_path+"Company_Data.xlsx", engine="openpyxl", usecols=cols)
            company_data_dump = company_data_df.rename(columns=col_rename)
            company_data_dump.to_sql(
                'company_table', con=db, if_exists='append')

        # Fetch data from tabless
        fund_data_df = pd.read_sql_query("SELECT * FROM df_table", db)
        company_data_df = pd.read_sql_query("SELECT * FROM company_table", db)
    return fund_data_df, company_data_df
