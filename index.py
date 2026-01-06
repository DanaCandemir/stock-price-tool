# import json
from time_series_stats import slice_52_wk, get_avg, low_high, fetch_data
# from db import seed_db, read_db, restore_daily


# with open('output.json', 'r') as f:
#     data = json.load(f)
#     sliced_data = slice_52_wk()
#     # avg = get_avg(sliced_data)
#     # print(avg)
#     # low_hi = low_high(sliced_data)

#     seed_db(sliced_data)


# read_db()

fetch_data("AAPL")

# print(slice_52_wk("NVDA"))
