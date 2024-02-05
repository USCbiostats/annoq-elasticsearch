import pickle
import time
import os
import argparse
from os import path as ospath
from src.config.base import write_to_json
from src.utils import id_gen

BATCH_SIZE = 50_000

def main():
    parser = parse_arguments()
    input_file = parser.input_file
    output_dir = parser.output_dir
    es_index = parser.es_index
    
    start_time = time.time()
    convert_file(input_file, output_dir, es_index, parser.doc_type_file)
    print("Process completed in ", time.time() - start_time, "seconds")



def parse_arguments():
    parser = argparse.ArgumentParser(description='File Conversion Tool')
    parser.add_argument('-i', '--input', dest='input_file', required=True, help='Path to the input file')
    parser.add_argument('-o', '--output', dest='output_dir', required=True, help='Path to the output directory')
    parser.add_argument('-m', '--doc_type_file', dest='doc_type_file', required=True, help='Document type mapping file')
    parser.add_argument('--es_index', dest='es_index', required=True, help='Elasticsearch index name')
    return parser.parse_args()


def init_find_error():
    err_file = open("log_import_error", "w")

    def t(da):
        for i in da:
            err_file.write(str(i) + "\n")
    return t


def tmp_print(*argv):
    s = ' '.join((str(i) for i in argv))
    print('\b'*tmp_print.l + ' '*tmp_print.l, end='\r', flush=True)
    print(s, end='', flush=True)
    tmp_print.l = len(s)


def parse_line(line, data_parser, header):
    d = {}
    for idx, key in enumerate(header):
        if idx < len(line) and line[idx] != "":
            try:
                d[key] = data_parser.get(key, str)(line[idx])
            except Exception as e:
                print('Parse error:', key, line[idx], data_parser.get(key, str))
                d[key] = str(line[idx])
    return d


def convert_file(in_filepath, out_dir, es_index, doc_type_file):   
    with open(doc_type_file, 'rb') as data:
        dtype = pickle.load(data)

    data_parser = {}
    for k in dtype:
        data_parser[k] = eval(dtype[k])
    data_parser['chr'] = str
    data_parser['GWAS_catalog_pubmedid'] = str
    data_parser['GRASP_PMID'] = str

    count = 0
    out_filename = 1
    header = ''
    da_list = []
   
    with open(in_filepath) as fp:
        row = fp.readline().rstrip()
              
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
            da_list.append(data)
            if count % BATCH_SIZE == 0:
                write_to_json(da_list, ospath.join(out_dir, str(out_filename) + '.json'),  indent=2)
                out_filename += 1
                da_list = []
                tmp_print("Processed", count, "records. Time elapsed:", time.time() - start_time, "s")
                
        write_to_json(da_list, ospath.join(out_dir, str(out_filename) + '.json'),  indent=2)
       
        print("import records ", count)
        print("used time", time.time() - start_time, "s")


if __name__=='__main__':
    find_error = init_find_error()
    start_time = time.time()
    tmp_print.l = 0

    main()
    
    find_error = init_find_error()
    start_time = time.time()
        