#!/usr/bin/env python
# -*- coding: utf8 -*-

from ramboo_tools.stream_processor import StreamProcessor
from ramboo_tools.pretty_printer import pp


class PrettyPrintStreamProcessor(StreamProcessor):
    """
    优雅的打印对象，对括号进行多行展开
    """

    def rows_process(self, rows=None, *objects, **kwargs):
        field_num_list = self.cmd_args.get('field_num_list')
        if not field_num_list:
            field_num_list = [self.cmd_args.get('field_num', 1)]
        fold_line = self.cmd_args.get('fold_line', 30)
        format_str = self.cmd_args.get('format_str', True)
        keep_str = not format_str
        for field_num in field_num_list:
            content = str(rows[field_num - 1])
            rows[field_num - 1] = pp(content, fold_line=fold_line, keep_str=keep_str)
        print(*rows, sep=self.separator, file=self.output_stream)
        return None

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        parser.add_argument('-fold', '--fold_line', default=30, type=int, help='fold content over this much lines. 30 default, set 0 to disable')
        parser.add_argument('--format_str', action='store_true', help='wether to format str in content')


def main():
    PrettyPrintStreamProcessor().stream_process()


if __name__ == '__main__':
    main()
