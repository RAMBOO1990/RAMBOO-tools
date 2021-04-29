#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@Time    : 2018-08-02
@Author  : RAMBOO
@Desc    : csv转txt 使用csv库实现
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import io

# 第三方库
import six
import csv

# 内部库
from ramboo_tools.stream_processor import StreamProcessor


class CsvToTextStreamProcessor(StreamProcessor):

    def __init__(self):
        super().__init__()
        self.keep_input = False

    def _before_process(self, *objects, **kwargs):
        csv_delimiter = self.cmd_args.get('csv_delimiter', ',')
        csv_encoding = self.cmd_args.get('csv_encoding', 'gbk')
        self.input_stream = csv.reader(
            io.TextIOWrapper(self.input_stream.buffer, encoding=csv_encoding),
            delimiter=csv_delimiter
        )

    def _get_rows_from_line(self, line, separator, encoding, *objects, **kwargs):
        return line

    def rows_process(self, rows=None, *objects, **kwargs):
        if self.input_stream.line_num == 1:
            return None
        if six.PY2:
            rows = [six.ensure_str(rows) for row in rows]
        return rows

    def _add_cmd_args(self, parser):
        parser.add_argument('-d', '--csv_delimiter', default=',', type=str, help='input csv delimiter')
        parser.add_argument('-e', '--csv_encoding', default='gbk', type=str, help='input csv encoding, gbk defalut')


def main():
    processorObj = CsvToTextStreamProcessor()
    processorObj.stream_process(**processorObj.get_cmd_args())


if __name__ == '__main__':
    main()
