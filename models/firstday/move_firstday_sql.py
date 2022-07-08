

import os
import glob
import logging


if __name__ == '__main__':
    SQL_EXT = '.sql'
    dir_name = '../mimic-code/mimic-iii/concepts/firstday'
    target_dir_name = './models/firstday'
    for fn in glob.glob(os.path.join(dir_name, '*%s' % SQL_EXT)):
        if not os.path.isfile(fn):
            logging.debug('skipping file %s' % fn)
            continue
        
        # print(os.path.basename(fn))
        file_name = os.path.basename(fn)
        table_name = os.path.splitext(file_name)[0]
        # /Users/chenchunyu/Documents/workspace/Experiment/mimic/mimic/seeds/ADMISSIONS.csv
        # command = f"""\copy {table_name.lower()} from '~/Documents/workspace/Experiment/mimic/mimic/seeds/{file_name}' with (FORMAT csv, DELIMITER ',', QUOTE '"', ESCAPE '\\', header)"""
        # print(command)
        # print(fn)
        with open(fn) as f:
            sql_query = f.read()
            sql_query = sql_query.replace('physionet-data.mimiciii_clinical.', '')
            sql_query = sql_query.replace('physionet-data.mimiciii_derived.', '')
            if 'physionet-data.mimiciii_derived.' in sql_query:
                print(file_name)
            sql_query = sql_query.replace('physionet-data.mimiciii_notes.', '')
            sql_query = sql_query.replace('`', "")
            sql_query = sql_query.replace(';', "")
            # if sql_query.endswith(';'):
            #     print(file_name)
            #     print('--' *50)
            #     sql_query = sql_query[ :-2]

            fp = open(os.path.join(target_dir_name, file_name), "w")
            fp.write(sql_query)
            fp.close()