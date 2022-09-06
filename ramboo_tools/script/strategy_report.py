#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
from typing import OrderedDict
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
        parser.add_argument('-lt', '--label_target', type=str, help='若有值，将label值转换为int(label==label_target)的0/1标签')
        parser.add_argument('-pt', '--predict_target', type=str, help='若有值，将predict值转换为int(predict==predict_target)的0/1标签。若为len，转换为int(len(predict_target))')
        # parser.add_argument('-t', '--target', type=str, help='common target (as label_target & predict_target)')
        parser.add_argument('-ls', '--labels_skip', action='append', type=str, default=[], help='skip label values (append)')
        parser.add_argument('-ps', '--predicts_skip', action='append', type=str, default=['-', 'error'], help='skip predict values (append)')
        parser.add_argument('-s', '--skip', type=str, default=[], help='common skip (as labels_skip & predicts_skip)')
        parser.add_argument('-l', '--label_names', action='append', type=str, help='label names(append)')
        parser.add_argument('-v', '--verbose', action='store_true', help='whether to print detail info')
        parser.add_argument('-k', '--output_keys', action='append', help='output keys(append), all keys default')
        parser.add_argument('-pk', '--print_key', action='store_true', help='whether to print key(<key:value> instead <value> only)')

    def _before_process(self, *args, **kwargs):
        self.y_actual_list = []
        self.y_predict_list = []

    def _convert_label_predict(self, label, predict, labels_skip, label_target, predicts_skip, predict_target):
        assert label.lower() not in labels_skip, f'skip label[{label.lower()}]'
        if label_target is not None:
            label = label == label_target
        label = int(label)
        assert predict.lower() not in predicts_skip, f'skip predict[{predict.lower()}]'
        if predict_target == 'len':
            predict = bool(len(predict))
        elif predict_target is None:
            pass
        else:
            predict = predict_target == predict
        predict = int(predict)
        return label, predict

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
        verbose = self.cmd_args.get('verbose', False)
        if not verbose:
            self.raise_row_error = True
        try:
            label, predict = self._convert_label_predict(label, predict, labels_skip, label_target, predicts_skip, predict_target)
        except Exception:
            if verbose:
                raise
            return None
        self.y_actual_list.append(label)
        self.y_predict_list.append(predict)
        if verbose:
            return label, predict
        return None

    def _after_process(self, *args, **kwargs):
        label_names = self.cmd_args.get('label_names')
        assert len(self.y_actual_list) == len(self.y_predict_list), f'label_n[{len(self.y_actual_list)}] res_n[{len(self.y_predict_list)}] unmatch'
        report_dict = metrics.classification_report(
            self.y_actual_list,
            self.y_predict_list,
            target_names=label_names,
            digits=4,
            output_dict=True,
            zero_division=0,
        )
        verbose = self.cmd_args.get('verbose', False)
        if verbose:
            logging.info(json.dumps(report_dict, indent=4))
        else:
            logging.debug(json.dumps(report_dict, indent=4))
        # output precision / recall
        output = OrderedDict()
        for classes, report in report_dict.items():
            if classes in ['macro avg', 'weighted avg']:
                continue
            if isinstance(report, dict) and 'precision' in report and 'recall' in report:
                precision = float('%.4f' % report['precision'])
                recall = float('%.4f' % report['recall'])
                f1_score = float('%.4f' % report['f1-score'])
                logging.debug(f'label[{classes}] precision[{precision}] recall[{recall}]')
                output.update(
                    {
                        f"label-{classes}-precision": "{:.2%}".format(precision),
                        f"label-{classes}-recall": "{:.2%}".format(recall),
                        f"label-{classes}-f1_score": "{:.2%}".format(f1_score),
                    }
                )
        output['accuracy'] = "{:.2%}".format(report_dict['accuracy'])
        output_keys = self.cmd_args.get('output_keys')
        if output_keys:
            output = {key: output.get(key, self.rows_result_default) for key in output_keys}
            self.fixed_column_width = len(output_keys)
        if self.cmd_args.get('print_key'):
            res = [f'{key}({type(value).__name__}):{value}' for key, value in output.items()]
        else:
            res = list(output.values())
        print(*res, sep='\t')


def main():
    StrategyReportProcessor().stream_process()


if __name__ == '__main__':
    main()
