#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
from ramboo_tools.stream_processor import StreamProcessor
from ramboo_tools import util


class OverwriteStreamProcessor(StreamProcessor):
    """
    读取覆盖数据，覆盖输入的数据后输出
    """

    fixed_column_width = 0

    def _add_cmd_args(self, parser):
        parser.add_argument('-over', '--overwrite_file', type=str, help='覆盖数据(文本,tab分割)')
        parser.add_argument('-k', '--key', type=str, help='覆盖数据中，构成key的列号，支持多列，逗号分割')
        parser.add_argument('-v', '--value', type=int, help='覆盖数据中，覆盖的列号（会用这个值覆盖其他值），逗号分割')
        return super()._add_cmd_args(parser)

    def _before_process(self, *args, **kwargs):
        keys_fields = list(map(int, self.cmd_args.get('key', '').split(',')))
        if not keys_fields:
            raise ValueError('key is empty')
        field_num_list = self.cmd_args.get("field_num_list")
        assert len(field_num_list) == len(keys_fields), f'key len unmatch [{len(field_num_list)}](-fl) [{len(keys_fields)}](-k)'
        value_field = self.cmd_args.get('value')
        overwrite_file_path = self.cmd_args.get('overwrite_file')
        overwrite_file, self.need_close = util.get_file_obj(overwrite_file_path)
        self.overwrite_dict = {}
        for line in overwrite_file:
            rows = line.split('\t')
            overwrite_value = rows[value_field - 1]
            key = '_'.join([rows[key_field - 1] for key_field in keys_fields])
            self.overwrite_dict[key] = overwrite_value

    def rows_process(self, rows=None, *objects, **kwargs):
        field_num = self.cmd_args.get("field_num", 1)
        field_num_list = self.cmd_args.get("field_num_list", [])
        key = '_'.join([rows[field_num - 1] for field_num in field_num_list])
        msg = 'unmatch'
        if key in self.overwrite_dict:
            overwrite_valule = self.overwrite_dict[key]
            raw_value = rows[field_num - 1]
            msg = 'match_unchange' if raw_value == overwrite_valule else f'match_changed from {raw_value}'
            rows[field_num - 1] = overwrite_valule
            return msg
        return msg


def main():
    OverwriteStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
