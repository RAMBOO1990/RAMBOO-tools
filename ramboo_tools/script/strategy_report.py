#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from sklearn import metrics

from ramboo_tools.stream_processor import StreamProcessor


class StrategyReportProcessor(StreamProcessor):
    """
    策略指标报告
    """

    rows_result_default = ['ERROR']

    def __init__(self):
        super().__init__()

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        parser.add_argument('-f2', '--field_num_2', default=2, type=int, help='startegy res field num')
        parser.add_argument('-lt', '--label_target', type=str, help='convert label to 0/1(match target or not)')
        parser.add_argument(
            '-st', '--strategy_target', type=str, help='convert res to 0/1(match target or not). <value>: res==value[default] / len: len(res)'
        )
        parser.add_argument('-l', '--label_names', action='append', type=str, help='label names(append)')

    def _before_process(self, *args, **kwargs):
        self.y_actual_list = []
        self.y_predict_list = []

    def rows_process(self, rows, *objects, **kwargs):
        field_num = self.cmd_args.get('field_num', 1)
        label = rows[field_num - 1]
        startegy_res_field = self.cmd_args.get('field_num_2', 2)
        startegy_res = rows[startegy_res_field - 1]
        label_target = self.cmd_args.get('label_target')
        strategy_target = self.cmd_args.get('strategy_target')
        if label_target is not None:
            label = label == label_target
        label = int(label)
        if startegy_res.lower() in ['-', 'error']:
            return None
        if strategy_target == 'len':
            startegy_res = bool(len(startegy_res))
        elif strategy_target is None:
            pass
        else:
            startegy_res = strategy_target == startegy_res
        startegy_res = int(startegy_res)
        if self.line_count <= 10:
            logging.debug(f'rows:{rows} label[{label}] startegy_res[{startegy_res}]')
        self.y_actual_list.append(label)
        self.y_predict_list.append(startegy_res)
        return None

    def _after_process(self, *args, **kwargs):
        label_names = self.cmd_args.get('label_names')
        assert len(self.y_actual_list) == len(self.y_predict_list), f'label_n[{len(self.y_actual_list)}] res_n[{len(self.y_predict_list)}] unmatch'
        report = metrics.classification_report(self.y_actual_list, self.y_predict_list, target_names=label_names, digits=4)
        print(report, file=self.output_stream)


def main():
    processorObj = StrategyReportProcessor()
    processorObj.stream_process()


if __name__ == '__main__':
    main()
