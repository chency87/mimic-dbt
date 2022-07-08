result = """"""

result_single_worker = ''''''
import numpy as np
from matplotlib import pyplot as plt
import re
from datetime import datetime
import glob, os
import logging

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

def plot_cdf(arr, x_label, y_label, title, label, worker_count):
    label_arr = ['.', 'o', '+', 'd']
    line_color = ['b', 'g', 'r', 'c', 'm', 'y','k']

    N = len(arr)
    x = np.sort(arr)
    y = np.arange(N) / float(N)
    # plotting
    plt.xlabel(x_label) # 'Query Duration(sec)'
    plt.ylabel(y_label) # 'CDF'
    plt.title(title) # 'CDF: duration of each query'
    idx = int(worker_count)%len(label_arr)
    line_color_idx = int(worker_count)%len(line_color)

    plt.plot(x, y, marker=label_arr[idx], label = label, color= line_color[line_color_idx]) # "CDF"



def get_results():
    dir_name = './_python_result_analyze/dbt_results_text/model_59'
    RESULT_EXT = '.txt'
    for fn in glob.glob(os.path.join(dir_name, '*%s' % RESULT_EXT)):
        if not os.path.isfile(fn):
            logging.debug('skipping file %s' % fn)
            continue
        file_name = os.path.basename(fn)
        with open(fn) as f:
            dbt_result_txt = f.read()
            metadata = parse_dbt_result(dbt_result_txt)
            worker_count = re.search(r'_(\d+)_worker', file_name).group(1)
            # print(worker_count.group(1))
            # plot_cdf_for_each_query(metadata, worker_count)
            plot_cdf_for_all_query(metadata, worker_count)
    plt.legend()
    plt.show()

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


def plot_cdf_for_each_query(query_metadata, worker_count):
    exec_time_array = []
    for item in query_metadata.values():
        exec_time_array.append(item.get('duration'))
    plot_cdf(exec_time_array, 'Query Duration(sec)', 'CDF', 'CDF: duration of each query', f'CDF (workers: {worker_count})', worker_count)

def plot_cdf_for_all_query(query_metadata, worker_count):
    tasks_start_time = query_metadata.get('query_1').get('query_start_time')
    exec_time_array = []
    for item in query_metadata.values():
        query_start_time = item.get('query_start_time')
        duration = item.get('duration')
        sub = (query_start_time - tasks_start_time).total_seconds()
        # print(f'{sub} + {duration} = {sub + duration}')
        exec_time_array.append(sub + duration)
    plot_cdf(exec_time_array, 'Query Duration(sec)', 'CDF', 'CDF: duration of all query', f'CDF (workers: {worker_count})', worker_count)



if __name__ == '__main__':
    # ringle_worker_metadata = parse_dbt_result(result_single_worker)
    # plot_cdf_for_each_query(ringle_worker_metadata)
    get_results()
    # metadata = parse_dbt_result(result)
    
    # plot_cdf_for_all_query(metadata)