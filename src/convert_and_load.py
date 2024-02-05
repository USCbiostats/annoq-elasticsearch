'''
usage: convert_to_json.py <gzfile>.gz [folder]

it will convert gz file into multiple json files and put them in ./json/[folder/]<gzfile>/1 ./json/[folder/]<gzfile>/2...

'''
import sys
import time
import os
from src.convert_to_json import convert_file, create_working_dir, delete_working_dir
from src.index_es_json import bulk_load

in_folder = sys.argv[1]

work_directory = 'temp_work_load'
start_time = time.time()

for root, dirs, files in os.walk(in_folder, topdown=False):
    for name in files:
        if name.endswith('.gz'):
            create_working_dir(work_directory)
            filepath = os.path.join(root, name)
            print(filepath)
            convert_file(filepath, work_directory)
            bulk_load(work_directory)
            print("finished ", filepath, time.time() - start_time, "s")
            delete_working_dir(work_directory)

print("")
print("used time", time.time() - start_time, "s")
