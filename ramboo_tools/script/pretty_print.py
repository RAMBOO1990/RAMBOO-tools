#!/usr/bin/env python
# -*- coding: utf8 -*-

from ramboo_tools.stream_processor import StreamProcessor
from ramboo_tools.pretty_printer import pp


class PrettyPrintStreamProcessor(StreamProcessor):
    """
    优雅的打印对象（主要对括号进行多行展开）
    """

    def rows_process(self, rows=None, *objects, **kwargs):
        field_num = int(self.cmd_args.get('field_num', 1))
        content = str(rows[field_num - 1])
        rows[field_num - 1] = pp(content)
        print(*rows, sep=self.separator, file=self.output_stream)
        return None


def main():
    processorObj = PrettyPrintStreamProcessor()
    processorObj.stream_process()


if __name__ == '__main__':
    main()
