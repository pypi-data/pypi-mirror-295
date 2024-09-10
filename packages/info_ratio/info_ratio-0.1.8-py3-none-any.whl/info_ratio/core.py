from datetime import datetime
import pandas as pd
from tqdm import tqdm
from info_ratio.common.input_output import dfs_tabs
from info_ratio.common.logging import loga
from info_ratio.common.helper_functions import preprocess_data, calculate_information_ratio


pd.options.mode.chained_assignment = None  # default='warn'


@loga
class InfoRatio:
    def __init__(self, db_path, out_path, start_date, end_date, data_insert_path=None, insert_data=False, enable_logging=True):

        if not enable_logging:
            loga.stop()

        self.dfs = []
        self.only_wins = []
        self.only_losses = []
        self.dont_exist = []
        self.only_win_df_fin = self.only_loss_df_fin = self.dont_exist_df_fin = pd.DataFrame()
        self.sheets = ['Only Wins', 'Only Losses', "No Data Found"]

        self.insert_data = insert_data

        self.start_date = start_date
        self.end_date = end_date

        self.db_path = db_path
        self.out_path = out_path
        self.data_insert_path = data_insert_path

    @loga.ignore
    def run(self):
        processed_df = preprocess_data(self)
        print("Total Number of Funds: ", len(
            processed_df["Scheme Name"].unique()))
        for category in tqdm(processed_df["Sub Nature"].unique()):
            print("Calculating Info Ratio for Category: ", category)
            category_df = processed_df[processed_df["Sub Nature"] == category]
            scheme_names = category_df["Scheme Name"].unique()
            print("Number of Schemes: ", len(scheme_names))
            category_fund_info = []
            for scheme_name in tqdm(scheme_names):
                print(scheme_name)
                fund_info = [scheme_name]
                scheme_df = processed_df[processed_df["Scheme Name"]
                                         == scheme_name]
                fund_info, type_ = calculate_information_ratio(
                    scheme_df, fund_info)
                if type_ == 0:
                    self.only_losses.append(fund_info)
                elif type_ == 1:
                    self.only_wins.append(fund_info)
                elif type_ == 3:
                    category_fund_info.append(fund_info)
                elif type_ == 4:
                    self.dont_exist.append(fund_info)
            category_df = pd.DataFrame(category_fund_info, columns=['Fund Name', 'Breadth', 'Wins', 'Loss', "Batting Average",
                                                                    "Slugging Ratio", "Information Coefficient", "Information Ratio", "Pain/Gain Ratio"])
            sorted_cat_df = category_df.sort_values(
                'Information Ratio', ascending=False)
            self.sheets.insert(0, category)
            self.dfs.insert(0, sorted_cat_df)

        only_win_df = pd.DataFrame(self.only_wins, columns=[
            'Fund Name', 'Breadth'])
        only_loss_df = pd.DataFrame(self.only_losses, columns=[
                                    'Fund Name', 'Breadth'])
        dont_exist_df = pd.DataFrame(self.dont_exist, columns=['Fund Name'])

        final_dfs = self.dfs + [only_win_df, only_loss_df, dont_exist_df]
        name = self.out_path+"InfoRatio_" + \
            datetime.today().strftime("%Y-%m-%d") + ".xlsx"
        dfs_tabs(final_dfs, self.sheets, name)

        return "Done !"
