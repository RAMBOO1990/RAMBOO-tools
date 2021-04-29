#!/usr/bin/env python
# encoding=utf-8

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys
import json

# 第三方库
from six.moves.html_parser import HTMLParser

# 内部库
from feed_antispam_lib.util import print
from feed_antispam_lib import util
from feed_antispam_lib import stream_processor
from feed_antispam_lib import global_data
from feed_antispam_lib import emoji_info


class HtmlUnescape(stream_processor.StreamProcessor):
    """
    Html编码转换
    """

    def __init__(self):
        """
        初始化
        """
        self.parser = HTMLParser()

    def rows_process(self, rows, *objects, **kwargs):
        """
        处理输入流的一行数据，将会被stream_process()方法调用，返回结果将输出至输出流
        rows: 接收输入流的一行数据
        *objects, **kwargs: 接受其余参数
        """
        res = []
        for row in rows:
            # 修复贴吧 emoji bug，如：&#xF40E; -> &#x1F40E;
            row = emoji_info.fix_tieba_bug(row)
            res.append(self.parser.unescape(row))
            if global_data.is_debug:
                res.append(self.parser.unescape(row).encode('unicode_escape'))
        return res

    def get_unittest_text_list(self):
        """
        提供单元测试数据
        """
        return [
            r'🐎',
            r'&#xF40E;',
            r'&#x1F40E;',
            r'❤️',
            r'&#x2764;&#xFE0F;',
            r'最好的王凯&#x2764;&#xFE0F;&#x2764;&#xFE0F;',
            r'穿AJ的都这么喜欢秀鞋子&#xF40E;？',
            r'做这个的都是穷批&#xF40E;',
            r'ヽ(爱&#x00B4;&#x2200;‘爱)ノ',
            r'做低调人，做高调事，此所谓人上人。助你东山再起，再创辉煌。【叩&#xD4E5; 同步】跟着队伍一起发展~7o^1&#xD7F1;^81&#x0B68;~一起闯出个未来~！队员每月平均收入14&#xD4E6;~',
            r'坐等农大征集或填二批比较&#xF42E;的。',
            r'作为一个男的声音这样还*别人的母&#xF602;你自己听到自己声音不会软么',
        ]


def main():
    """
    主程序
    """
    import argparse
    parser = argparse.ArgumentParser(description='Html编码转换')
    parser.add_argument('-i', '--input', default=sys.stdin, help='input file name')
    parser.add_argument('-o', '--output', default=sys.stdout, help='output file name')
    parser.add_argument('-s', '--separator', default='\t', help='i/o stream separator, \\t default')
    parser.add_argument('-enc', '--encoding', default='utf-8', help='input encoding')
    parser.add_argument('-ut', '--unittest', action='store_true', help='unit test')
    args = parser.parse_args()

    htmlUnescapeObj = HtmlUnescape()

    if args.unittest:
        htmlUnescapeObj.unittest()
        return
    htmlUnescapeObj.stream_process(
        args.input, args.output, separator=args.separator, encoding=args.encoding, keep_input=False
    )


if __name__ == '__main__':
    main()
