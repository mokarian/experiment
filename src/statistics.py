"""
This file contains modules used to calculate the statistics for a src engine
"""
import os
from enum import Enum
from os import walk
import pandas as pd

from src.constants import Constants
from src.utils import Utils


def already_processed(subset):
    file_name = '-'.join(subset)
    file_name = os.path.join('generated', file_name + '.csv')
    # print("subset number " + str(len([name for name in os.listdir('.') if os.path.isfile(file_name)])) + " is done : ")
    return os.path.isfile(file_name)


def read_generated_files_to_list():
    statistics = []
    f = []
    for (dirpath, dirnames, filenames) in walk("generated"):
        f.extend(filenames)
    for a_file in filenames:
        df = pd.read_csv(os.path.join("generated", a_file))
        fn = len(df.loc[df['result'] == 'FN'])
        tp = len(df.loc[df['result'] == 'TP'])
        tn = len(df.loc[df['result'] == 'TN'])
        fp = len(df.loc[df['result'] == 'FP'])
        analyzers = os.path.splitext(a_file)[0]
        statistics.append({"fn": fn, "tp": tp, "tn": tn, "fp": fp, "fields": analyzers})
    return statistics

class Statistics:
    """
    This class contains methods to calculate the statistics for a src index
    """

    def __init__(self):
        self.utils = Utils(os.path.join("resources"))

    def mark_confusion_matrix(self, expected, retrieved):
        """
        this method calculates the confusion matrix based on expected and retrieved results
        :param expected:  expected name
        :param retrieved:   what retrieved from the src engine
        :return:  TP or FP or TN or FN
        """
        if self.is_true_positive(expected, retrieved):
            return Result.TP
        if self.is_false_positive(expected, retrieved):
            return Result.FP
        if self.is_true_negative(expected, retrieved):
            return Result.TN
        if self.is_false_negative(expected, retrieved):
            return Result.FN

        raise Exception(
            'expected:{} name and retrieved:{} name does not belong'
            ' to any of the TN,FP,TF,FN categories'.format(
                expected, retrieved))

    @staticmethod
    def is_true_positive(expected_name, retrieved_name):
        """
        this method determines if the result is TP
        TP - Some name found and it matches expected name
        :param expected_name:
        :param retrieved_name:
        :return:
        """
        return expected_name == retrieved_name \
               and expected_name != "NOT_FOUND" \
               and retrieved_name != "NOT_FOUND"

    @staticmethod
    def is_false_positive(expected_name, retrieved_name):
        """
        this method determines if the result is FP
        FP - Some name found but it does not match expected name
        :param expected_name:
        :param retrieved_name:
        :return:
        """
        return expected_name != retrieved_name \
               and ((expected_name != "NOT_FOUND" and retrieved_name != "NOT_FOUND")
                    or (expected_name == "NOT_FOUND" and retrieved_name != "NOT_FOUND"))

    @staticmethod
    def is_true_negative(expected_name, retrieved_name):
        """
        this method determines if the result is TN
        TN - No name found and no expected name
        :param expected_name:
        :param retrieved_name:
        :return:
       """
        return expected_name == retrieved_name \
               and expected_name == "NOT_FOUND" \
               and retrieved_name == "NOT_FOUND"

    @staticmethod
    def is_false_negative(expected_name, retrieved_name):
        """
        this method determines if the result is FP
        FN - No name found but there was expected name
        :param expected_name:
        :param retrieved_name:
        :return:
        """

        return expected_name != retrieved_name \
               and expected_name != "NOT_FOUND" \
               and retrieved_name == "NOT_FOUND"

    @staticmethod
    def calc_precision(true_positive, false_positive):
        """
        Calculate the results precision.

        Keyword arguments:
        true_positive(int) - count of true positive results
        false_positive(int) - count of false positive results
        """
        if true_positive + false_positive == 0:
            print("Precision undefined (Divide by zero)")
            return -1
        return true_positive / (true_positive + false_positive)

    @staticmethod
    def calc_recall(true_positive, false_negative):
        """
        Calculate the results recall.

        Keyword arguments:
        true_positive(int) - count of true positive results
        false_negative(int) - count of false positive results
        """
        if true_positive + false_negative == 0:
            print("Recall undefined  (Divide by zero)")
            return -1
        return true_positive / (true_positive + false_negative)

    @staticmethod
    def f1_score(precision, recall):
        """
        Calculates an F1 score based on the precision and recall results.

        Keyword arguments:
        precision(double) - calculated precision from true_positives and false_positives.
        recall(double) - calculated recall from true_positives and false_negatives.
        """
        if precision + recall == 0:
            print("F1 undefined  (Divide by zero)")
            return -1
        return 2 * precision * recall / (precision + recall)

    def calculate_statistics(self, correct_list,
                             misspelled_list,
                             subsets,
                             search_engine,
                             generate_reports=False):
        """
        This function calculates different metrics for each fields and returns
        a list of the results accordingly.
        pseudo code:
        <p>
        for each item in misspelled_items:
            for each filed combination
                send_query_to_search_engine
             calculate tp, tn, fp, fn, precision, precision and f1
             store the metrics in a list
        </p>
        :param search_engine: the target src engine (Elastic, Azure)
        :param correct_list: list of correct items
        :param misspelled_list:   list of misspelled items
        :param subsets:  a subset of all  combinations of different fields.
        we send a src request to each of those subsets
        :param generate_reports: if true, it create individual report files per field
        :return: a list of the results
        """
        fields_statistics = []
        print("total subsets: " + str(len(subsets)))
        for subset in subsets:

            if already_processed(subset):
                continue
            DIR = 'generated'
            print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
            true_positive = 0
            true_negative = 0
            false_positive = 0
            false_negative = 0
            data = []
            for i in range(0, len(misspelled_list)):
                retrieved = search_engine.make_search(misspelled_list[i][0], list(subset))
                expected = correct_list[i][0]
                result = Statistics().mark_confusion_matrix(expected, retrieved).value
                if result == Result.TP.value:
                    true_positive += 1
                elif result == Result.TN.value:
                    true_negative += 1
                elif result == Result.FP.value:
                    false_positive += 1
                elif result == Result.FN.value:
                    false_negative += 1

                data_object = {
                    Constants.retrieved: retrieved,
                    Constants.expected: expected,
                    Constants.result: result}

                data.append(data_object)

            file_name = '-'.join(subset)
            if generate_reports:
                self.utils.generate_reports(data, file_name)

    @staticmethod
    def generate_f1():
        statistics = read_generated_files_to_list()
        for stat in statistics:
            stat["precision"] = Statistics.calc_precision(stat["tn"], stat["fp"])
            stat["recall"] = Statistics.calc_recall(stat["tp"], stat["fn"])
            stat["f1"] = Statistics.f1_score(stat["precision"], stat["recall"])
        return statistics


class Result(Enum):
    """
    This is an enumeration type for:
    TN:   True Negative
    FN:   False Negative
    TP:   True Positive
    FP:   False Positive
    """
    TN = "TN"
    FN = "FN"
    TP = "TP"
    FP = "FP"
