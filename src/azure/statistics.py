"""
This file contains modules used to calculate the statistics for azure src
"""
import os
from src.utils import Utils
from matplotlib import pyplot as plt


def create_plot():
    UTILS = Utils(os.path.join("resources"))
    json_file = UTILS.read_json_from_resources("reports.json")
    sorted_on_f1 = UTILS.sort_on_f1_score(json_file, False)
    f1 = []
    precision = []
    recall = []
    keep_item = False
    for item in sorted_on_f1:
        if item["fields"] == "standard_lucene":
            keep_item = True
        if keep_item:
            f1.append(item["f1"])
            precision.append(item["precision"])
            recall.append(item["recall"])
    fig = plt.figure()

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    # ax.set_title('axes title')

    ax.set_xlabel('Analyzers with F1 higher than default(standard_lucene)')
    ax.set_ylabel('F1 Score')
    ax.plot(f1, label='recall')
    ax.annotate('F1 score: 0.69', xy=(70, 55),
                arrowprops=dict(facecolor='yellow', shrink=0.01),
                xycoords='figure points',
                xytext=(70, 200),
                )

    ax.annotate('F1 score: 0.74', xy=(422, 308),
                arrowprops=dict(facecolor='green', shrink=0.01),
                xycoords='figure points',
                xytext=(329, 100),
                )

    # ax.plot(precision, label='precision')
    # ax.legend(['y = recall', 'y = precision'], loc='center left')
    plt.show()
    pass


if __name__ == '__main__':
    # UTILS = Utils(os.path.join("resources"))
    # FIELDS = Constants.company_search_fields
    # ALL_SUBSETS = UTILS.get_subsets(FIELDS)
    #
    # MISSPELLED__COMPANY_NAMES = UTILS.read_csv("names-misspelled.csv")
    #
    # NAMES_MORE_THAN_ONE_ELEMENT = []
    #
    # CORRECT_COMPANY_NAMES = UTILS.read_csv("names-expected.csv")
    # azure = Azure()
    #
    # STATISTICS = Statistics().calculate_statistics(CORRECT_COMPANY_NAMES,
    #                                                MISSPELLED__COMPANY_NAMES,
    #                                                ALL_SUBSETS, azure,
    #                                                generate_reports=True)
    # STATISTICS = Statistics().generate_f1()
    #
    # UTILS.write_json_to_directory(STATISTICS, "reports")
    # print(UTILS.get_shortest_fields_with_highest_f1_score(STATISTICS))
    create_plot()
