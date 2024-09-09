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
def get_data(db, insert_data=False):
    if insert_data:
        # Define the path to the Excel file
        file_uploads = ["info_ratio/data/Holdings Historical 360 to DSP.xlsx",
                        "info_ratio/data/Holdings Historical Edelweiss to Invesco.xlsx",
                        "info_ratio/data/Holdings Historical ITI to PPFAS.xlsx",
                        "info_ratio/data/Holdings Historical Quant to Zerodha.xlsx"]

        # Loop through each Excel file in 'file_uploads'
        for i in file_uploads:
            dfs = pd.read_excel(i, engine="openpyxl", skiprows=4)
            dfs.to_sql('df_table', con=db, if_exists='append')

        cols = ['CD_ISIN No', 'Bmonth_Month End', 'Bmonth_Close']
        col_rename = {'CD_ISIN No': 'Company ISIN',
                      'Bmonth_Month End': 'Numeric Date', 'Bmonth_Close': 'Price'}
        company_data_df = pd.read_excel(
            "info_ratio/data/Company_Data.xlsx", engine="openpyxl", usecols=cols)
        company_data_dump = company_data_df.rename(columns=col_rename)
        company_data_dump.to_sql('company_table', con=db, if_exists='append')

        return db
    else:
        return db
