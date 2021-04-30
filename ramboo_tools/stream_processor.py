#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import argparse
import logging

import six

from . import util
from .util import print


class StreamProcessor(object):
    """
    流式处理器基类，支持以标准I/O流形式处理数据，默认I/O编码utf-8
    """

    def __init__(self):
        """
        初始化
        """
        self.cmd_args = self.get_cmd_args()
        self.need_split_line = True

    def _before_process(self, *objects, **kwargs):
        """
        前置钩子
        """
        pass

    def _after_process(self, *objects, **kwargs):
        """
        后置钩子
        """
        pass

    def _before_stream_process_rows(self, line, *objects, **kwargs):
        """
        行处理前置钩子
        """
        return line

    def _get_rows_from_line(self, line, separator, encoding, *objects, **kwargs):
        """
        从line获取rows
        """
        line = six.ensure_text(line, encoding=encoding).strip('\n')
        rows = line.split(separator)
        return rows

    def rows_process(self, rows=None, *objects, **kwargs):
        """
        处理输入流的一行数据，将会被stream_process()方法调用，返回结果将输出至输出流
        rows: 接收输入流的一行数据
        *objects, **kwargs: 接受其余参数
        """
        raise NotImplementedError('StreamProcessor基类方法，需子类继承StreamProcessor后实现')

    def stream_process(
        self, input_stream=None, output_stream=None,
        separator='\t', encoding='utf-8', keep_input=True,
        *objects, **kwargs
    ):
        """
        流式处理
        从input_stream中读取数据，通过separator分割为rows，调用stream_process_rows()方法处理，得到的结果写入output_stream
        keep_input: 是否在输出流中保留输入数据（保留时，每行处理结果将会附加在末尾列）
        encoding: I/O编码，默认utf-8
        *objects, **kwargs: 接收其余参数，透传至内部处理方法
        """
        close_file_list = []
        self.input_stream, close_input = util.get_file_obj(input_stream, 'r', sys.stdin)
        if close_input:
            close_file_list.append(self.input_stream)
        self.output_stream, close_output = util.get_file_obj(output_stream, 'w', sys.stdout)
        if close_output:
            close_file_list.append(self.output_stream)

        self.keep_input = keep_input

        self._before_process(*objects, **kwargs)
        self.line_count = 0
        for line in self.input_stream:
            try:
                if not line:
                    continue
                self.line_count += 1
                line = self._before_stream_process_rows(line, *objects, **kwargs)
                if self.need_split_line:
                    rows = self._get_rows_from_line(line, separator, encoding, *objects, **kwargs)
                res = self.rows_process(rows, *objects, **kwargs)
                if res is None:
                    continue
                if not isinstance(res, (list, tuple)):
                    res = [res]
                output_rows = rows if self.keep_input else []
                output_rows.extend(res)
                print(*output_rows, sep=separator, encoding=encoding, file=self.output_stream)
            except Exception as error:
                logging.exception(error)
                continue
        self._after_process(*objects, **kwargs)
        for file_to_close in close_file_list:
            file_to_close.close()

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        pass

    def get_cmd_args(self, return_dict=True):
        """
        获取并转换命令行参数
        """
        parser = argparse.ArgumentParser(
            description='stream processor')
        parser.add_argument(
            '--input_stream', default=sys.stdin, type=argparse.FileType('r'), help='input file/stream')
        parser.add_argument(
            '--output_stream', default=sys.stdout, type=argparse.FileType('w'), help='output file/stream')
        parser.add_argument(
            '--seperator', default='\t', help=r'i/o rows seperator, \t default')
        parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
        parser.add_argument(
            '-f', '--field_num', default=1, type=int, help='input content row number, 1 default')
        self._add_cmd_args(parser)

        args = parser.parse_args()
        res = args.__dict__ if return_dict else args
        return res

    @property
    def unittest_text_list(self):
        """
        提供单元测试数据
        """
        return [
            r'hello world',
            r'单元测试',
            r'unittest_text_list用于提供单元测试数据，子类可覆盖该方法提供测试数据'
        ]

    def unittest(self, *objects, **kwargs):
        """
        单元测试
        """
        text_list = [six.ensure_binary(text, encoding='utf-8') for text in self.unittest_text_list]
        self.stream_process(text_list, *objects, **kwargs)
