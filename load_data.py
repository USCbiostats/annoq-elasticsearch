from elasticsearch import Elasticsearch
from elasticsearch import helpers
import fileinput
import pickle
from utils import id_gen
from collections import deque
import sys
import time
from setup_es import *



def init_find_error():
    err_file = open("log_import_error","w")
    def t(es, da):
         for i in da:
             try: 
                 es.index(id=i['_id'], index=i['_index'], body=i['_source'])
             except: 
                 err_file.write( str(i) + "\n")
                 print('import error !')
    return t


find_error = init_find_error()
start_time = time.time()
if len(sys.argv) > 1:
    skip = int(sys.argv[1])
else:
    skip = 0

def tmp_print(*argv):
    s = ' '.join((str(i) for i in argv))
    print('\b'*tmp_print.l + ' '*tmp_print.l, end = '\r', flush=True)
    print(s, end='', flush=True)
    tmp_print.l = len(s)
tmp_print.l = 0

def parse_line(l, data_parser, header):
    line = l.rstrip().split("\t")
    d = {}
    for idx in range(len(header)):
        if line[idx] == ".":
            continue
        k = header[idx]
        try:
            d[k] = data_parser.get(k, str)(line[idx])
        except:
            print('parse error:',k, line[idx], data_parser.get(k, str))
            d[k] = str(line[idx])
    return d



data = open('data/doc_type.pkl', 'rb')
dtype = pickle.load(data)
data_parser = {}
for k in dtype:
    data_parser[k] = eval(dtype[k])
data_parser['chr'] = str
data_parser['GWAS_catalog_pubmedid'] = str
data_parser['GRASP_PMID'] = str

error = open("error.log", "w")
header = ''
count = 0
da_list = []

def fake(*argv, **karg):
    pass
deque = fake
def helper():
    h = helpers.streaming_bulk
helper = helpers.parallel_bulk
skipped = 0
for i in sys.stdin:
    if skipped < skip:
        skipped += 1
        continue
    count += 1
    if not header:
        header = i.rstrip().split("\t")
        continue
    data = {
        "_index": "annoq-test",
        "_id": id_gen(i),
        "_source": parse_line(i, data_parser, header)
    }
    try:
        data = {
        "_index": "annoq-test",
        "_id": id_gen(i),
        "_source": parse_line(i, data_parser, header)
    }
        da_list.append(data)
    except:
        error.write(i)
    if count % 5000 == 0:
        try:
            h = helper(es, da_list, chunk_size=500 )
            deque(h, maxlen=0)
        except:
            find_error(es, da_list)
        da_list = []
        tmp_print("import {}".format(count), "spend time:", time.time() - start_time, "s")
try:
    h = helper(es, da_list, chunk_size=500 )
    deque(h, maxlen=0)
except:
    find_error(es, da_list)
print("")
print("import record ", count)
print("used time", time.time() - start_time,"s")
