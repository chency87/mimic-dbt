result = """03:30:45  1 of 33 START table model public.adenosine_durations ........................... [RUN]
03:30:45  2 of 33 START table model public.arterial_line_durations ....................... [RUN]
03:30:45  3 of 33 START table model public.central_line_durations ........................ [RUN]
03:30:45  4 of 33 START table model public.code_status ................................... [RUN]
03:30:48  1 of 33 OK created table model public.adenosine_durations ...................... [SELECT 160 in 3.03s]
03:30:48  5 of 33 START table model public.crrt_durations ................................ [RUN]
03:30:51  2 of 33 OK created table model public.arterial_line_durations .................. [SELECT 30487 in 6.78s]
03:30:51  6 of 33 START table model public.dobutamine_dose ............................... [RUN]
03:30:52  3 of 33 OK created table model public.central_line_durations ................... [SELECT 38510 in 6.93s]
03:30:52  7 of 33 START table model public.dobutamine_durations .......................... [RUN]
03:30:52  5 of 33 OK created table model public.crrt_durations ........................... [SELECT 5918 in 4.38s]
03:30:52  8 of 33 START table model public.dopamine_dose ................................. [RUN]
03:30:54  4 of 33 OK created table model public.code_status .............................. [SELECT 61532 in 9.65s]
03:30:54  9 of 33 START table model public.dopamine_durations ............................ [RUN]
03:30:59  6 of 33 OK created table model public.dobutamine_dose .......................... [SELECT 6548 in 7.48s]
03:30:59  10 of 33 START table model public.echo_data .................................... [RUN]
03:30:59  7 of 33 OK created table model public.dobutamine_durations ..................... [SELECT 1792 in 7.35s]
03:30:59  11 of 33 START table model public.elixhauser_ahrq_v37 .......................... [RUN]
03:31:00  8 of 33 OK created table model public.dopamine_dose ............................ [SELECT 38953 in 7.48s]
03:31:00  12 of 33 START table model public.elixhauser_ahrq_v37_no_drg ................... [RUN]
03:31:00  9 of 33 OK created table model public.dopamine_durations ....................... [SELECT 6524 in 5.40s]
03:31:00  13 of 33 START table model public.elixhauser_quan .............................. [RUN]
03:31:00  12 of 33 OK created table model public.elixhauser_ahrq_v37_no_drg .............. [SELECT 58976 in 0.71s]
03:31:00  14 of 33 START table model public.epinephrine_dose ............................. [RUN]
03:31:00  11 of 33 OK created table model public.elixhauser_ahrq_v37 ..................... [SELECT 58976 in 1.45s]
03:31:00  15 of 33 START table model public.epinephrine_durations ........................ [RUN]
03:31:04  13 of 33 OK created table model public.elixhauser_quan ......................... [SELECT 58976 in 4.53s]
03:31:04  16 of 33 START table model public.icustay_detail ............................... [RUN]
03:31:05  16 of 33 OK created table model public.icustay_detail .......................... [SELECT 61051 in 0.49s]
03:31:05  17 of 33 START table model public.icustay_times ................................ [RUN]
03:31:08  15 of 33 OK created table model public.epinephrine_durations ................... [SELECT 3126 in 8.07s]
03:31:08  18 of 33 START table model public.isuprel_durations ............................ [RUN]
03:31:09  14 of 33 OK created table model public.epinephrine_dose ........................ [SELECT 10565 in 8.50s]
03:31:09  19 of 33 START table model public.milrinone_durations .......................... [RUN]
03:31:11  10 of 33 OK created table model public.echo_data ............................... [SELECT 45794 in 12.16s]
03:31:11  20 of 33 START table model public.neuroblock_dose .............................. [RUN]
03:31:12  17 of 33 OK created table model public.icustay_times ........................... [SELECT 61532 in 6.96s]
03:31:12  21 of 33 START table model public.norepinephrine_dose .......................... [RUN]
03:31:14  18 of 33 OK created table model public.isuprel_durations ....................... [SELECT 26 in 5.14s]
03:31:14  22 of 33 START table model public.norepinephrine_durations ..................... [RUN]
03:31:14  19 of 33 OK created table model public.milrinone_durations ..................... [SELECT 3600 in 5.64s]
03:31:14  23 of 33 START table model public.phenylephrine_dose ........................... [RUN]
03:31:18  20 of 33 OK created table model public.neuroblock_dose ......................... [SELECT 9978 in 6.59s]
03:31:18  24 of 33 START table model public.phenylephrine_durations ...................... [RUN]
03:31:20  21 of 33 OK created table model public.norepinephrine_dose ..................... [SELECT 161539 in 8.37s]
03:31:20  25 of 33 START table model public.vasopressin_dose ............................. [RUN]
03:31:21  22 of 33 OK created table model public.norepinephrine_durations ................ [SELECT 23188 in 7.63s]
03:31:21  26 of 33 START table model public.vasopressin_durations ........................ [RUN]
03:31:23  23 of 33 OK created table model public.phenylephrine_dose ...................... [SELECT 186281 in 8.34s]
03:31:23  27 of 33 START table model public.vasopressor_durations ........................ [RUN]
03:31:25  24 of 33 OK created table model public.phenylephrine_durations ................. [SELECT 33141 in 7.62s]
03:31:25  28 of 33 START table model public.ventilation_classification ................... [RUN]
03:31:31  25 of 33 OK created table model public.vasopressin_dose ........................ [SELECT 10537 in 10.45s]
03:31:31  29 of 33 START table model public.ventilation_durations ........................ [RUN]
03:31:31  26 of 33 OK created table model public.vasopressin_durations ................... [SELECT 4190 in 9.45s]
03:31:31  30 of 33 START table model public.weight_durations ............................. [RUN]
03:31:37  27 of 33 OK created table model public.vasopressor_durations ................... [SELECT 38832 in 14.51s]
03:31:37  31 of 33 START table model public.elixhauser_score_ahrq ........................ [RUN]
03:31:37  31 of 33 OK created table model public.elixhauser_score_ahrq ................... [SELECT 58976 in 0.12s]
03:31:37  32 of 33 START table model public.elixhauser_score_quan ........................ [RUN]
03:31:38  32 of 33 OK created table model public.elixhauser_score_quan ................... [SELECT 58976 in 0.25s]
03:31:41  29 of 33 OK created table model public.ventilation_durations ................... [SELECT 38509 in 10.82s]
03:31:43  30 of 33 OK created table model public.weight_durations ........................ [SELECT 1016671 in 11.98s]
03:31:43  33 of 33 START table model public.heightweight ................................. [RUN]
03:31:45  28 of 33 OK created table model public.ventilation_classification .............. [SELECT 2549354 in 19.88s]
03:31:45  33 of 33 OK created table model public.heightweight ............................ [SELECT 61532 in 2.62s]"""

# runnint time : \d+:\d+:\d+
from cProfile import label
import numpy as np
from matplotlib import pyplot as plt
import re
from datetime import datetime

# res = result.split('\n')
# re_runnint_time = r'\d+:\d+:\d+'
# re_index_of_query = r'(\d+\sof\s\d+\sOK).*in\s(\d+\.\d+)s'
# re_exec_time = r'\d+\.\d+s'

# re_exp_ok = r'(\d+:\d+:\d+)\s*(\d+)\sof\s(\d+)\sOK.*in\s(\d+\.\d+)s'
# re_exp_start = r'(\d+:\d+:\d+)\s*(\d+)\sof\s(\d+)\sSTART.*'

# exec_time_array = []

def parse_dbt_result(dbt_result):
    re_exp_ok = r'(\d+:\d+:\d+)\s*(\d+)\sof\s(\d+)\sOK.*in\s(\d+\.\d+)s'
    re_exp_start = r'(\d+:\d+:\d+)\s*(\d+)\sof\s(\d+)\sSTART.*'
    res = dbt_result.split('\n')
    query_result_metadata = {}
    for item in res:
        # match = re.search(re_index_of_query, item)
        query_start_match = re.search(re_exp_start, item)
        query_ok_match = re.search(re_exp_ok, item)
        if query_start_match:
            
            query_start_time = query_start_match.group(1)
            query_start_time = datetime.strptime(query_start_time, '%H:%M:%S')
            query_index = query_start_match.group(2)
            total_query = query_start_match.group(3)        
            query_result_metadata[f'query_{query_index}'] = {'query_start_time': query_start_time, 'total_query': total_query}
        if query_ok_match:
            query_end_tiem = datetime.strptime(query_ok_match.group(1), '%H:%M:%S')
            query_index = query_ok_match.group(2)
            total_query = query_ok_match.group(3)
            query_duration = query_ok_match.group(4)
            query_result_metadata.get(f'query_{query_index}')['duration'] = float(query_duration)
            query_result_metadata.get(f'query_{query_index}')['query_end_tiem'] = query_end_tiem
    # print(query_result_metadata)
    return query_result_metadata


def plot_cdf_for_each_query(query_metadata):
    exec_time_array = []
    for item in query_metadata.values():
        exec_time_array.append(item.get('duration'))
    
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    N = len(exec_time_array)
    x = np.sort(exec_time_array)
    y = np.arange(N) / float(N)

    # plotting
    plt.xlabel('Query Duration(sec)')
    plt.ylabel('CDF')
    plt.title('CDF: duration of each query')
    plt.plot(x, y, marker='o', label = "CDF")
    plt.legend()
    plt.show()


def plot_cdf_for_all_query(query_metadata):
    tasks_start_time = query_metadata.get('query_1').get('query_start_time')

    pass

#     if match:
#         query_start_time = ''

#         running_time = item[0:item.index(match.group())].strip()

#         running_time = datetime.strptime(running_time, '%H:%M:%S')
#         query_index = match.group()[0:match.group().index(' ')]
#         exec_time = match.group(2)
#         print(f"running time: {running_time}")
#         # print(f"Query Index: {query_index}")
#         # print(f"exec time: {exec_time}")
#         exec_time_array.append(float(exec_time))
        
#         # print(item.index(match.group()))
#         # print(item[item.index(match.group()):-1])

# # exec_time_array = exec_time_array.astype(float)

# plt.show()




if __name__ == '__main__':
    metadata = parse_dbt_result(result)
    plot_cdf_for_each_query(metadata)