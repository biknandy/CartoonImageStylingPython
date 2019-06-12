import csv


def load_csv(filename):
    lines = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            lines.append(line)
    return lines


def extract_features(raw):
    val_names = raw.pop(0)
    data_set = []
    for row in raw:
        data_point = {}
        vals = []
        data_point['country'] = row[0]
        for r in row[1:]:
            vals.append(float(r))
        data_point['vals'] = vals
        data_set.append(data_point)
    return val_names, data_set


def load_data():
    lines = load_csv("country.csv")
    return extract_features(lines)
    #returns val_names and data_set
    #data set is an array of dict, each with 'country' and array of 'vals'
