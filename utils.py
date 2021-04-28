def id_gen(l):
    line = l.rstrip().split("\t")
    return "{}:{}{}>{}".format(line[0], line[1], line[2], line[3])
