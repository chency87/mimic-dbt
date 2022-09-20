import psycopg2
import glob
import os
MODEL_DIR = './models'
MODEL_EXT = '.sql'
# './_python_result_analyze/dbt_results_text'
#establishing the connection


def del_models_in_dir(dir_name):
   print( f'Processing model: {dir_name}')
   print('**' *15)
   for fn in os.listdir(dir_name):
      if os.path.isdir(os.path.join(dir_name, fn)):
         del_models_in_dir(os.path.join(dir_name, fn))
   for sql_fn in glob.glob(os.path.join(dir_name, '*%s' % MODEL_EXT)):
      if not os.path.isfile(sql_fn):
         continue
      file_name = os.path.basename(sql_fn)
      table_name = os.path.splitext(file_name)[0]
      try:
         cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
      except Exception as e:
         cursor.execute(f"DROP view IF EXISTS {table_name} CASCADE")
      print(f"Table: {table_name} dropped... ")
if __name__ == '__main__':
   conn = psycopg2.connect(
      database="mimic", user='chunyu', password='chunyu', host='127.0.0.1', port= '5432'
   )

   #Setting auto commit false
   conn.autocommit = True

   #Creating a cursor object using the cursor() method
   cursor = conn.cursor()
   del_models_in_dir(MODEL_DIR)
   #Commit your changes in the database
   conn.commit()
   #Closing the connection
   conn.close()