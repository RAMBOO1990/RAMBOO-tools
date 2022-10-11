#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import jq
from ramboo_tools.stream_processor import StreamProcessor


class JqStreamProcessor(StreamProcessor):
    """
    封装[jq](https://github.com/mwilliamson/jq.py)，加入多列处理
    """

    fixed_column_width = 0

    def _add_cmd_args(self, parser):
        parser.add_argument('-jq', type=str, help='jq program string, see https://stedolan.github.io/jq/manual/')
        return super()._add_cmd_args(parser)

    def rows_process(self, rows=None, *objects, **kwargs):
        jq_str = self.cmd_args.get('jq', '.')
        field_num = self.cmd_args.get('field_num', 1)
        json_str = rows[field_num - 1]
        json_data = json.loads(json_str)
        res = jq.compile(jq_str).input(json_data).all()
        return res


def main():
    JqStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
