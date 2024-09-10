import loga
import asyncio
import numpy as np
import pandas as pd
from datetime import datetime
from info_ratio.common.logging import loga
from info_ratio.common.input_output import get_data


@loga.errors
def preprocess_data(self):
    start = pd.Timestamp(self.start_date)
    end = pd.Timestamp(self.end_date)
    fund_data_df, company_data_df = get_data(
        self, insert_data=self.insert_data)

    fund_data_df['Numeric Date'] = fund_data_df['Port Date'].apply(
        lambda x: datetime.strptime(x, "%d-%b-%Y").strftime("%Y%m")).astype(np.int64)

    # Merge single_fund_df with ace_df_renamed on 'Company ISIN' and 'Numeric Date'
    # Use 'left' join to keep all rows from single_fund_df and fill in 'Price' where matches are found
    merged_df = pd.merge(fund_data_df, company_data_df, on=[
                         'Company ISIN', 'Numeric Date'], how='left')
    merged_df["No Of Shares"] = merged_df["No Of Shares"].replace(
        '--', None, regex=True)

    # Drop rows where 'Price' and 'No of Shares'is missing
    merged_df = merged_df[merged_df['Price'].notna()]
    merged_df = merged_df[merged_df["No Of Shares"].notna()]

    # Convert 'Port Date' to a datetime object
    merged_df['Port Date_'] = pd.to_datetime(merged_df['Port Date'])
    merged_df = merged_df.sort_values(by='Port Date_')
    merged_df["No Of Shares"] = merged_df["No Of Shares"].astype(int)
    merged_df = merged_df.loc[merged_df['Port Date_'].between(start, end)]

    return merged_df


def run_in_parallel(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


@run_in_parallel
def calculate_stock_info(input_df, stock_name):
    stock_df = input_df[input_df['Company Name'] == stock_name]
    if len(stock_df) < 2:
        # print("Stock Name with less data point:", stock_name)
        return None

    stock_df["diff_tmp"] = stock_df["No Of Shares"].diff()
    stock_df["ret_tmp"] = stock_df["Price"] * stock_df["diff_tmp"]
    stock_df['ret_tmp'].iloc[0] = stock_df['Price'].iloc[0] * \
        stock_df['No Of Shares'].iloc[0]

    # We are assuming the the portfolio manager has exited the remaining shares at the end of the analysis period
    last_exit = stock_df['Price'].iloc[-1] * \
        stock_df['No Of Shares'].iloc[-1]

    sum_of_positive_nos = stock_df[stock_df['ret_tmp']
                                   >= 0]['ret_tmp'].sum()

    sum_of_negative_nos = np.abs(stock_df[stock_df['ret_tmp'] <= 0]
                                 ['ret_tmp']).sum() + last_exit

    if sum_of_positive_nos < sum_of_negative_nos:
        stock_absolute_gain = round((sum_of_negative_nos -
                                     sum_of_positive_nos), 3)
        return [1, 0, stock_absolute_gain, 0]
    else:
        stock_absolute_loss = round((sum_of_negative_nos -
                                     sum_of_positive_nos), 3)
        return [0, 1, 0, stock_absolute_loss]


@loga.errors
def calculate_information_ratio(input_df, fund_info):

    # Get the breadth of the fund
    stock_list = input_df['Company Name'].unique()

    # Have a new event loop
    loop = asyncio.get_event_loop()

    looper = asyncio.gather(*[calculate_stock_info(input_df, i)
                            for i in stock_list])  # Run the loop

    results = loop.run_until_complete(looper)

    results_notna = [x for x in results if x is not None]

    breadth = len(results_notna)
    if breadth == 0:
        return fund_info, 4
    fund_info.append(breadth)

    summed_result = [sum(x) for x in zip(*results_notna)]
    num_wins, num_losses, absolute_gain, absolute_loss = summed_result

    if num_wins == 0:
        return fund_info, 0
    else:
        average_gain = abs(absolute_gain)/num_wins
    if num_losses == 0:
        return fund_info, 1
    else:
        average_loss = abs(absolute_loss)/num_losses

    fund_info.append(num_wins)
    fund_info.append(num_losses)

    # Pain-to-Gain Ratio
    pain_gain_ratio = abs(absolute_gain/absolute_loss)

    # Calculate the batting average
    batting_average = num_wins/breadth
    fund_info.append(round(batting_average, 3))

    # Calculate the slugging ratio
    slugging_ratio = average_gain/average_loss

    fund_info.append(round(slugging_ratio, 3))

    information_coefficient = 1.6*(batting_average - (1/(1+slugging_ratio)))
    fund_info.append(round(information_coefficient, 3))

    information_ratio = information_coefficient * (np.sqrt(breadth))
    fund_info.append(round(information_ratio, 3))
    fund_info.append(round(pain_gain_ratio, 3))

    return fund_info, 3
