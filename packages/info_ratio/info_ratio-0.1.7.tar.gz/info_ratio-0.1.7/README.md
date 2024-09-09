To Run:

from info_ratio.common.input_output import dfs_tabs
from info_ratio.core import InfoRatio

out_ = '/home/rolf/Music/Results/'
db_path_ = "/home/rolf/Music/MutualFundData.db"

ir = InfoRatio(db_path_, out_,
               start_date='2023-07-01', end_date='2024-07-01')
ir.run()