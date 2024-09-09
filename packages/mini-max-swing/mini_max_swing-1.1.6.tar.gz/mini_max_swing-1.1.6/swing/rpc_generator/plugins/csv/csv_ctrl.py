"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:57
@Author: xingyun
"""
import csv
from collections import namedtuple


class CsvCtrl:

    @staticmethod
    def create_csv(file_path, head=None):
        with open(file_path, 'w', encoding='utf-8') as f:
            csv_write = csv.writer(f, quoting=csv.QUOTE_ALL)
            if head:
                csv_write.writerow(head)
        return file_path

    @staticmethod
    def read_csv(file_path, ignore_head=True):
        counter = 0
        csv.field_size_limit(500 * 1024 * 1024)
        f = csv.reader(open(file_path, 'r', encoding='utf-8'))
        for line in f:
            if ignore_head:
                if counter:
                    yield line
                counter += 1
            else:
                yield line

    @staticmethod
    def read_csv_zip(file_path):
        f = csv.reader(open(file_path, 'r', encoding='utf-8'))
        headers = next(f)
        for line in f:
            yield zip(headers, line)

    @staticmethod
    def get_csv_head(file_path):
        f = csv.reader(open(file_path, 'r', encoding='utf-8'))
        for line in f:
            return line

    @staticmethod
    def append_lines(file_path, lines):
        with open(file_path, 'a', encoding='utf-8-sig') as f:
            csv_write = csv.writer(f, quoting=csv.QUOTE_ALL)
            csv_write.writerows(lines)

    @staticmethod
    def get_rows_with_type(file_path, col_types):
        with open(file_path, 'r', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            Row = namedtuple('Row', headers)
            for r in f_csv:
                _row = []
                row = Row(*r)
                for convert, value in zip(col_types, row):
                    if convert == list:
                        _v = eval(value)
                    else:
                        _v = convert(value)
                    _row.append(_v)
                yield _row


if __name__ == "__main__":
    csv_ctrl = CsvCtrl()
    line = [["234353", "sdgdg",
             "[sdgdggsd]",
             "{'a':1}", 344454, "0", 34545, 99, 'sdgsdgds']]
