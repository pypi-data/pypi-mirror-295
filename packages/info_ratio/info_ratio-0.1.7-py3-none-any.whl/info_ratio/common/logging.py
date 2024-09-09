from loga import Loga

# all setup values are optional
loga = Loga(
    facility="info_ratio",  # name of program logging the message
    do_print=True,  # print each log to console
    truncation=1000,  # longest possible value in extra data
    private_data={"password"},  # set of sensitive args/kwargs
)


# @loga.errors
# def calculate_information_ratio(input_df, fund_info):

#     num_wins = 0
#     num_losses = 0
#     absolute_gain = 0
#     absolute_loss = 0

#     # Get the breadth of the fund
#     stock_list = input_df['Company Name'].unique()
#     breadth = len(stock_list)
#     if breadth == 0:
#         return fund_info, 4
#     fund_info.append(breadth)

#     for i in stock_list:
#         stock_df = input_df[input_df['Company Name'] == i]
#         stock_df["diff_tmp"] = stock_df["No Of Shares"].diff()
#         stock_df["ret_tmp"] = stock_df["Price"] * stock_df["diff_tmp"]
#         stock_df['ret_tmp'].iloc[0] = stock_df['Price'].iloc[0] * \
#             stock_df['No Of Shares'].iloc[0]

#         # We are assuming the the portfolio manager has exited the remaining shares at the end of the analysis period
#         last_exit = stock_df['Price'].iloc[-1] * \
#             stock_df['No Of Shares'].iloc[-1]

#         sum_of_positive_nos = stock_df[stock_df['ret_tmp']
#                                        >= 0]['ret_tmp'].sum()

#         some_of_negative_nos = np.abs(stock_df[stock_df['ret_tmp'] <= 0]
#                                       ['ret_tmp']).sum() + last_exit

#         if sum_of_positive_nos < some_of_negative_nos:
#             num_wins += 1
#             absolute_gain += round((some_of_negative_nos -
#                                    sum_of_positive_nos), 3)
#         else:
#             num_losses += 1
#             absolute_loss += round((some_of_negative_nos -
#                                    sum_of_positive_nos), 3)

#     if num_wins == 0:
#         return fund_info, 0
#     else:
#         average_gain = abs(absolute_gain)/num_wins
#     if num_losses == 0:
#         return fund_info, 1
#     else:
#         average_loss = abs(absolute_loss)/num_losses

#     fund_info.append(num_wins)
#     fund_info.append(num_losses)

#     # Pain-to-Gain Ratio
#     pain_gain_ratio = abs(absolute_gain/absolute_loss)

#     # Calculate the batting average
#     batting_average = num_wins/breadth
#     fund_info.append(round(batting_average, 3))

#     # Calculate the slugging ratio
#     slugging_ratio = average_gain/average_loss

#     fund_info.append(round(slugging_ratio, 3))

#     information_coefficient = 1.6*(batting_average - (1/(1+slugging_ratio)))
#     fund_info.append(round(information_coefficient, 3))

#     information_ratio = information_coefficient * (np.sqrt(breadth))
#     fund_info.append(round(information_ratio, 3))
#     fund_info.append(round(pain_gain_ratio, 3))

#     return fund_info, 3
