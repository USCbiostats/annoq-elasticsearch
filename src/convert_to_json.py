import pickle
from utils import id_gen
import time
import os
import argparse
import shutil
import json
from os import path as ospath

def main():
    parser = parse_arguments()
    input_file = parser.input_file
    output_dir = parser.output_dir
    es_index = parser.es_index
    
    convert_file(input_file, output_dir, es_index)
    print("finished ",  time.time() - start_time, "s")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input_file', required=True,
                        help='Input folder')
    parser.add_argument('-o', '--output', dest='output_dir', required=True,
                        help='Output folder')
    parser.add_argument('--es_index', dest='es_index', required=True,
                        help='Index (annoq-test)')
   
    return parser.parse_args()


def init_find_error():
    err_file = open("log_import_error", "w")

    def t(da):
        for i in da:
            err_file.write(str(i) + "\n")
    return t


def write_to_json(filepath, jsons):
    with open(filepath, "w",  encoding='utf-8') as f:
        json.dump(jsons, f, indent=4)

def tmp_print(*argv):
    s = ' '.join((str(i) for i in argv))
    print('\b'*tmp_print.l + ' '*tmp_print.l, end='\r', flush=True)
    print(s, end='', flush=True)
    tmp_print.l = len(s)


def parse_line(line, data_parser, header):
    d = {}
    for idx in range(len(header)):
        if idx >= len(line) or line[idx] == "":            
            continue
        k = header[idx]
        try:
            d[k] = data_parser.get(k, str)(line[idx])
        except:
            print('parse error:', k, line[idx], data_parser.get(k, str))
            d[k] = str(line[idx])
    return d


def create_working_dir(directory):
    try:
        os.mkdir(directory)
        print(directory+ "(temp work directory) created\n")
    except:
        print('json path exists\n')


def delete_working_dir(directory):
    try:
        shutil.rmtree(directory)
        print(directory+"(temp work directory) removed\n")
    except:
        print('folder not removed\n')


def convert_file(in_filepath, out_dir, es_index):   
    with open('data/doc_type.pkl', 'rb') as data:
        dtype = pickle.load(data)

    data_parser = {}
    for k in dtype:
        data_parser[k] = eval(dtype[k])
    data_parser['chr'] = str
    data_parser['GWAS_catalog_pubmedid'] = str
    data_parser['GRASP_PMID'] = str

    error = open("error.log", "w")
    count = 0
    header = ''
    da_list = []
   
    with open(in_filepath) as fp:
        row = fp.readline().rstrip()
        out_filename = 1        
        header = row.split("\t")

        while row:
            row = fp.readline().rstrip()   
            if not row:
                continue
                 
            cols = row.split("\t")
            count += 1
            data = {
                "_index": es_index,
                "_id": id_gen(cols),
                "_source": parse_line(cols, data_parser, header)
            }
            try:
                data = {
                    "_index": es_index,
                    "_id": id_gen(cols),
                    "_source": parse_line(cols, data_parser, header)
                }
                da_list.append(data)
            except:
                error.write(cols)
            if count % 100000 == 0:
                write_to_json(ospath.join(out_dir, str(out_filename) + '.json'), da_list)
                out_filename += 1
                da_list = []
                tmp_print("import {}".format(count), "spend time:",
                        time.time() - start_time, "s")
        write_to_json(ospath.join(out_dir, str(out_filename) + '.json'), da_list)
       
        print("import records ", count)
        print("used time", time.time() - start_time, "s")


if __name__=='__main__':
    find_error = init_find_error()
    start_time = time.time()
    tmp_print.l = 0

    #main()
    
    find_error = init_find_error()
    start_time = time.time()
        