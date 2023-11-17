import io

from collections import OrderedDict
from django.http import FileResponse
import xlsxwriter
import openpyxl as xlsx
import csv
from ordered_set import OrderedSet


def is_orddict(value):
    return isinstance(value, list) and len(value) > 0 and isinstance(value[0], OrderedDict)


def get_headers(data):
    if len(data) == 0:
        return []

    headers = []
    for dicts in data:
        for key, value in dicts.items():
            if isinstance(value, list) and len(value) == 0:
                continue
            if is_orddict(value):
                headers.extend(f"{key}_{subkey}" for subkey in value[0])
            else:
                headers.append(key)

    return OrderedSet(headers)


def _write_ordered_dict_values(worksheet, values, start_row, start_col):
    offset = start_row
    for inner_obj in values:
        tmp_col = start_col
        for val in inner_obj.values():
            worksheet.write(start_row, tmp_col, val)
            tmp_col += 1
        start_row += 1
    offset = start_row - offset - 1
    return offset


def _write_list_values(worksheet, values, start_row, col):
    offset = start_row
    for val in values:
        worksheet.write(start_row, col, val)
        start_row += 1
    offset = start_row - offset - 1 if values else 0
    return offset


def _generate_xlsx(data):
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()

    headers = get_headers(data)
    for i, header in enumerate(headers):
        worksheet.write(0, i, header)

    row = 1
    offset = 0
    for obj in data:
        for col, key in enumerate(obj):
            value = obj[key]

            if isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], OrderedDict):
                    offset = _write_ordered_dict_values(worksheet, value, row, col)
                else:
                    offset = _write_list_values(worksheet, value, row, col)
            else:
                worksheet.write(row, col, value)
        row += 1 + offset

    workbook.close()
    buffer.seek(0)
    return buffer


def load_xlsx(data):
    buffer = _generate_xlsx(data)
    return FileResponse(buffer, as_attachment=True, filename='data.xlsx')


def load_csv(data):
    buffer = _generate_xlsx(data)
    excel = xlsx.load_workbook(buffer)
    sheet = excel.active

    csv_buff = io.StringIO()
    writer = csv.writer(csv_buff)
    for r in sheet.rows:
        writer.writerow([cell.value for cell in r])

    excel.close()
    csv_buff.seek(0)
    return FileResponse(io.BytesIO(csv_buff.read().encode('utf-8')), as_attachment=True, filename='data.csv')