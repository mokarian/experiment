"""
This file contains modules used to calculate the statistics for elastic src
"""
import os

from src.constants import Constants
from src.elastic.elastic import Elastic
from src.statistics import Statistics
from src.utils import Utils

if __name__ == '__main__':
    UTILS = Utils(os.path.join("resources"))
    FIELDS = Constants.name_search_fields
    ALL_SUBSETS = UTILS.get_subsets(FIELDS)
    MISSPELLED_NAMES = UTILS.read_csv("names-misspelled.csv")
    CORRECT_NAMES = UTILS.read_csv("names-expected.csv")
    elastic = Elastic()
    STATISTICS = Statistics().calculate_statistics(CORRECT_NAMES,
                                                   MISSPELLED_NAMES,
                                                   ALL_SUBSETS, elastic, generate_reports=True)
    Statistics().generate_f1()
    UTILS.write_json_to_directory(STATISTICS, "reports")
    print(UTILS.get_shortest_fields_with_highest_f1_score(STATISTICS))
