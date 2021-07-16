#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from sklearn import metrics

from ramboo_tools.stream_processor import StreamProcessor


class StrategyReportProcessor(StreamProcessor):
    """
    策略指标报告
    """

    fixed_column_width = 2

    def __init__(self):
        super().__init__()

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        parser.add_argument('-f2', '--field_num_2', default=2, type=int, help='startegy res field num')
        parser.add_argument('-lt', '--label_target', type=str, help='convert label to 0/1(match target or not)')
        parser.add_argument(
            '-pt', '--predict_target', type=str, help='convert res to 0/1(match target or not). <value>: res==value[default] / len: len(res)'
        )
        # parser.add_argument('-t', '--target', type=str, help='common target (as label_target & predict_target)')
        parser.add_argument('-ls', '--labels_skip', action='append', type=str, default=[], help='skip label values (append)')
        parser.add_argument('-ps', '--predicts_skip', action='append', type=str, default=['-', 'error'], help='skip predict values (append)')
        parser.add_argument('-s', '--skip', type=str, default=[], help='common skip (as labels_skip & predicts_skip)')
        parser.add_argument('-l', '--label_names', action='append', type=str, help='label names(append)')
        parser.add_argument('-d', '--need_detail', action='store_true', help='whether to print detail info')

    def _before_process(self, *args, **kwargs):
        self.y_actual_list = []
        self.y_predict_list = []

    def rows_process(self, rows, *objects, **kwargs):
        field_num = self.cmd_args.get('field_num', 1)
        label = rows[field_num - 1]
        predict_field_num = self.cmd_args.get('field_num_2', 2)
        predict = rows[predict_field_num - 1]
        label_target = self.cmd_args.get('label_target')
        predict_target = self.cmd_args.get('predict_target')
        skip = self.cmd_args.get('skip', [])
        predicts_skip = self.cmd_args.get('predicts_skip', ['-', 'error'])
        labels_skip = self.cmd_args.get('labels_skip', [])
        predicts_skip += skip
        labels_skip += skip
        need_detail = self.cmd_args.get('need_detail', False)
        if label.lower() in labels_skip:
            return '-', '-'
        if label_target is not None:
            label = label == label_target
        label = int(label)
        if predict.lower() in predicts_skip:
            return label, '-'
        if predict_target == 'len':
            predict = bool(len(predict))
        elif predict_target is None:
            pass
        else:
            predict = predict_target == predict
        predict = int(predict)
        self.y_actual_list.append(label)
        self.y_predict_list.append(predict)
        if need_detail:
            return label, predict
        return None

    def _after_process(self, *args, **kwargs):
        label_names = self.cmd_args.get('label_names')
        assert len(self.y_actual_list) == len(self.y_predict_list), f'label_n[{len(self.y_actual_list)}] res_n[{len(self.y_predict_list)}] unmatch'
        report = metrics.classification_report(self.y_actual_list, self.y_predict_list, target_names=label_names, digits=4)
        logging.debug(report)
        print(report, file=self.output_stream)


def main():
    processorObj = StrategyReportProcessor()
    processorObj.stream_process()


if __name__ == '__main__':
    main()
