import openpyxl
import json
import os
import config
from filter_map import into_json

class Record_xlsx():

    def __init__(self, record = None):
        self.mod = record[1]
        self.old_ip = record[4]
        self.new_ip = record[5]
        record[11] = str(record[11])
        self.record = record


def main():
    sheet = loading_worksheet(config.WORKSHEET)

    sheet_tmp = {}
    count = 0
    for record in sheet:
        sheet_tmp.update( **(record.__dict__.update({}'id': count))
        count += 1
    into_json(sheet_tmp, config.OUTPUTJSONEXCEL)

    return sheet


def loading_worksheet(name_sheet):
    sheet = []
    wb = openpyxl.load_workbook(config.HARDWARE)
    work_sheet = wb[name_sheet].rows
    description = []
    for row in work_sheet:
        loaded_row=[]

        if row[0].coordinate == 'A1':
            for desc in row:
                if desc.value != None:
                    description.append(desc.value)
                else:
                    description.append('')
            continue
        if not((row[5].value == '' or row[4].value =='') and row[2].font.strike):
            for cell in row:
                if cell.value is None:
                    cell.value = ''

                loaded_row.append(cell.value)
            sheet.append(Record_xlsx(loaded_row))
    return sheet

if __name__ == "__main__":
    main()
    print('done')