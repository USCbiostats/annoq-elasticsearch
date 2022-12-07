import json

def id_gen(line):
    return "{}:{}{}>{}".format(line[0], line[1], line[2], line[3])

def write_to_json(json_data, output_file, indent=None, cls=None):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, cls=cls, ensure_ascii=False, indent=indent)

def load_json(filepath):
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)