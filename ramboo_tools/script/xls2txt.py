#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@Time    : 2018-08-02
@Author  : RAMBOO
@Desc    : xls转txt 使用pandas库实现
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys

# 第三方库
import six
import pandas

# 内部库
from ramboo_tools.stream_processor import StreamProcessor


class XlsToTextStreamProcessor(StreamProcessor):

    def __init__(self):
        super().__init__()
        self.input_excel = self.cmd_args.get('input_excel', None)
        if not self.input_excel:
            raise ValueError('need -o input_excel')
        if self.input_excel == sys.stdin:
            raise TypeError('--input_excel must be file')
        if '.xls' not in self.input_excel.name:
            raise ValueError('input exceel file name must be xxx.xls(x)')
        data_frame = pandas.read_excel(self.input_excel.name, header=None)
        data_frame.fillna('', inplace=True)
        self.input_stream = data_frame.to_records(index=False)

    def _get_rows_from_line(self, line, separator, encoding, *objects, **kwargs):
        return line

    def stream_process_rows(self, rows=None, *objects, **kwargs):
        rows = [row.replace('\n', r'\n').replace('\t', r'\t') if isinstance(row, str) else row for row in rows]
        rows = [six.ensure_text(str(row)) for row in rows]
        return rows

    def _add_cmd_args(self, parser):
        import argparse
        parser.add_argument('-i', '--input_excel', required=True, type=argparse.FileType('r'), help='input excel file')


def main():
    processorObj = XlsToTextStreamProcessor()
    processorObj.stream_process()


if __name__ == '__main__':
    main()
