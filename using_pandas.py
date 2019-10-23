import pandas as pand
from filter_map import main as smart
import os
import config


def main():
    smart_map = smart()
    table = pand.DataFrame(columns=smart_map[0].__dict__.keys())
    for record in smart_map:
        record_arr = record.__dict__.values()
        table.loc[len(table)] = list(record_arr)
    table.loc[len(table)] = list(record_arr)

    output(table.to_json(orient='records'), config.TEST)
    double_table = table.duplicated('ip', keep=False)
    new_table = get_duplicate(table, double_table)
    output(new_table.to_json(orient='records'), config.TEST2)


def get_duplicate(table, index):

    new_table = pand.DataFrame(columns=table.columns.tolist())
    arr = index.tolist()

    for number, val in enumerate(arr):
        if val is True:
            new_table.loc[len(new_table)] = table.loc[number]

    return new_table


def output(obj, fname):
    if (os.path.isfile(fname)):
        os.remove(fname)

    with open(fname, 'a+', encoding='utf-8-sig') as test:
        test.write(obj)


if __name__ == "__main__":
    main()
