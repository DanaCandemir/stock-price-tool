import json
from time_series_stats import slice_52_wk, get_avg, low_high


with open('output.json', 'r') as f:
    data = json.load(f)
    sliced_data = slice_52_wk()
    avg = get_avg(sliced_data)
    print(avg)
    low_hi = low_high(sliced_data)
