#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
from typing import OrderedDict
from math import fabs
from sklearn import metrics

from ramboo_tools.stream_processor import StreamProcessor


class BinaryFindThresholdProcessor(StreamProcessor):
    """
    二分法确定策略阈值
    """

    fixed_column_width = 2

    def __init__(self):
        super().__init__()

    def _add_cmd_args(self, parser):
        """
        添加命令行参数，子类可覆盖该方法并调用parser.add_argument()添加参数
        """
        parser.add_argument('-lt', '--label_target', type=str, help='若有值，将label值转换为int(label==label_target)的0/1标签')
        # parser.add_argument('-t', '--target', type=str, help='common target (as label_target & predict_target)')
        parser.add_argument('-ls', '--labels_skip', action='append', type=str, default=[], help='skip label values (append)')
        parser.add_argument('-cs', '--score_skip', action='append', type=str, default=['-', 'error'], help='skip predict values (append)')
        parser.add_argument('-tp', '--target_precision', type=float, default=None, help='指定目标准确率，优先级高于指定召回率')
        parser.add_argument('-tr', '--target_recall', type=float, default=None, help='指定目标召回率')
        parser.add_argument('-s', '--skip', type=str, default=[], help='common skip (as labels_skip & score_skip)')
        parser.add_argument('-l', '--label_names', action='append', type=str, help='label names(append)')
        parser.add_argument('-v', '--verbose', action='store_true', help='whether to print detail info')
        parser.add_argument('-k', '--output_keys', action='append', help='output keys(append), all keys default')
        parser.add_argument('-pk', '--print_key', action='store_true', help='whether to print key(<key:value> instead <value> only)')

    def _before_process(self, *args, **kwargs):
        self.label_list = []
        self.score_list = []
        target_precision, target_recall = self.cmd_args.get('target_precision'), self.cmd_args.get('target_recall')
        assert target_precision or target_recall, 'both target_precision and target_recall is empty!'

    def _convert_label_score(self, label, score, labels_skip, label_target, score_skip):
        assert label.lower() not in labels_skip, f'skip label[{label.lower()}]'
        assert score.lower() not in score_skip, f'skip score[{score.lower()}]'
        if label_target is not None:
            label = label == label_target
        label, score = int(label), float(score)
        return label, score

    def rows_process(self, rows, *objects, **kwargs):
        field_num = self.cmd_args.get('field_num', 1)
        label = rows[field_num - 1]
        score_field_num = self.cmd_args.get('field_num_2', 2)
        score = rows[score_field_num - 1]
        label_target = self.cmd_args.get('label_target')
        skip = self.cmd_args.get('skip', [])
        score_skip = self.cmd_args.get('score_skip', ['-', 'error'])
        labels_skip = self.cmd_args.get('labels_skip', [])
        score_skip += skip
        labels_skip += skip
        verbose = self.cmd_args.get('verbose', False)
        if not verbose:
            self.raise_row_error = True
        try:
            label, score = self._convert_label_score(label, score, labels_skip, label_target, score_skip)
        except Exception:
            if verbose:
                raise
            return None
        self.label_list.append(label)
        self.score_list.append(score)
        if verbose:
            return label, score
        return None

    def _get_pr_by_class(self, label_list, score_list, threshold, target_class='1'):
        predict_list = [int(score > threshold) for score in score_list]
        report_dict = metrics.classification_report(
            label_list,
            predict_list,
            digits=4,
            output_dict=True,
            zero_division=0,
        )
        report = report_dict.get(target_class)
        assert isinstance(report, dict) and 'precision' in report and 'recall' in report
        precision = float('%.4f' % report['precision'])
        recall = float('%.4f' % report['recall'])
        f1_score = float('%.4f' % report['f1-score'])
        return precision, recall

    # 迭代次数上限
    STEP_LIMIT = 30
    # 目标准召误差上限
    ERROR_RANGE_LIMIT = 1e-3

    def bin_find_th(self, label_list, score_list, target_type, target_value):
        flag = -1 if target_type == 'precision' else 1
        left, right = 0, 1
        for step in range(self.STEP_LIMIT):
            current_th = float(left + right) / 2
            # 计算当前阈值下指标
            precision, recall = self._get_pr_by_class(label_list, score_list, current_th)
            logging_fun = logging.info if self.cmd_args.get('verbose', False) else logging.debug
            logging_fun(f'bin_find_th: current_th[{current_th}] left[{left}] right[{right}] precision[{precision}] recall[{recall}]')
            current_value = precision if target_type == 'precision' else recall
            # 迭代阈值
            error_value = fabs(current_value - target_value)
            if error_value < self.ERROR_RANGE_LIMIT:
                return current_th
            if (current_value - target_value) * flag > 0:
                # 提高准确，降低召回，阈值增加
                left = current_th
            else:
                # 降低准确，提高召回，阈值减小
                right = current_th
        logging.warning(f'cannot find best threshold for target in {self.STEP_LIMIT} steps, error_value[{error_value}]')
        return current_th

    def _after_process(self, *args, **kwargs):
        label_names = self.cmd_args.get('label_names')
        assert len(self.label_list) == len(self.score_list), f'label_num[{len(self.label_list)}] res_num[{len(self.score_list)}] unmatch'
        target_precision, target_recall = self.cmd_args.get('target_precision'), self.cmd_args.get('target_recall')
        target_type, target_value = ('precision', target_precision) if target_precision else ('recall', target_recall)
        threshold = self.bin_find_th(self.label_list, self.score_list, target_type=target_type, target_value=target_value)
        self.predict_list = [int(score > threshold) for score in self.score_list]
        report_dict = metrics.classification_report(
            self.label_list,
            self.predict_list,
            target_names=label_names,
            digits=4,
            output_dict=True,
            zero_division=0,
        )
        logging_fun = logging.info if self.cmd_args.get('verbose', False) else logging.debug
        logging_fun(json.dumps(report_dict, indent=4))
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
                        f"label-{classes}-precision": f"{precision:.2%}",
                        f"label-{classes}-recall": f"{recall:.2%}",
                        f"label-{classes}-f1_score": f"{f1_score:.2%}",
                    }
                )
        output['accuracy'] = f"{report_dict['accuracy']:.2%}"
        output['th'] = threshold
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
    BinaryFindThresholdProcessor().stream_process()


if __name__ == '__main__':
    main()
