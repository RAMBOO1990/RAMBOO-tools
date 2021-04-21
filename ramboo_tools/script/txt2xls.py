#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@Time    : 2018-06-06
@Author  : RAMBOO
@Desc    : txt转xls 使用pandas库实现
"""

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# 第三方库
import sys
import six
import pandas
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

# 内部库
from ramboo_tools.stream_processor import StreamProcessor


class TextToXlsStreamProcessor(StreamProcessor):

    def _before_process(self, *objects, **kwargs):
        if 'output_excel' not in kwargs:
            raise ValueError('need -o output_excel')
        self.output_excel = kwargs['output_excel']
        if self.output_excel == sys.stdout:
            raise TypeError('--output_excel must be file')
        if '.xls' not in self.output_excel.name:
            raise ValueError('output exceel file name must be xxx.xls(x)')
        self.column_name_list = kwargs.get('column_name', [])
        self.data_list = []

    def _before_stream_process_rows(self, line, *objects, **kwargs):
        line = ILLEGAL_CHARACTERS_RE.sub('', line)
        return line

    def stream_process_rows(self, rows=None, *objects, **kwargs):
        contain_table_head = bool(kwargs.get('table_head', False))
        if self.line_count == 1 and contain_table_head and self.column_name_list is None:
            self.column_name_list = rows
            return None
        if six.PY2:
            rows = [six.ensure_str(rows) for row in rows]
        self.data_list.append(rows)
        return None

    def _after_process(self, *objects, **kwargs):
        df = pandas.DataFrame(self.data_list, columns=self.column_name_list)
        df.to_excel(self.output_excel.name, sheet_name='Data', index=False)

    def _add_cmd_args(self, parser):
        import argparse
        parser.add_argument('-o', '--output_excel', required=True, type=argparse.FileType('w'), help='output file')
        parser.add_argument(
            '-th', '--table_head', action='store_true', default=False,
            help='whether to use the 1st line as table head'
        )
        parser.add_argument('-c', '--column_name', action='append', help='column names, overwrite `contain_table_head`')


def main():
    processorObj = TextToXlsStreamProcessor()
    processorObj.stream_process(**processorObj.get_cmd_args())


if __name__ == '__main__':
    main()
