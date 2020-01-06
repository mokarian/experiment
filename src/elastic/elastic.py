"""
This file contains methods to communicate with elastic src
"""
import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from src.utils import Utils


class Elastic:
    """
    This class contains methods to communicate with elastic src
    """

    def __init__(self):
        self.utils = Utils(os.path.join("resources"))
        self.config = self.utils.get_config()
        host = self.config["elastic"]['host']
        port = self.config["elastic"]['port']
        username = self.config["elastic"]['username']
        password = self.config["elastic"]['password']
        self.elastic_search = Elasticsearch("http://{}:{}@{}:{}".format(username, password, host, port))

    def add_user_names(self, index="indexname"):
        """
        this method adds documents to the src index.
        usernames are being loaded  from a CSV file and added separately
        :param index: index name
        """
        user_names = self.utils.read_csv()
        for name in user_names:
            body = {"name": name}
            self.elastic_search.index(index=index, body=body)

    def create_index(self, index_name="indexname", schema="index-schema.json"):
        """
        this method creates and index in the elastic src
        the created index is based on index-schema.json schema
        :param schema:schema of the index to be created
        :param index_name
        """
        self.elastic_search.indices.create(index=index_name,
                                           body=self.utils.read_json_from_resources(schema))

    def make_search(self, misspelled_name, fields, index_name="indexname"):
        """
        this method queries the elastic src index
        :param index_name:
        :param fields:
        :param misspelled_name:
        :query  the query
        """
        body = self.utils.create_elastic_search_body(misspelled_name, fields)
        search = Search(using=self.elastic_search).index(index_name).update_from_dict(body)
        response = search.execute()
        return self.utils.get_maximum_rank_from_elastic_search_response(response)

    def add_statistics_to_index(self, report_file="reports.json"):
        """
        This method is to add statistics to a new index in the elastic src
        :param report_file: a json file created by statistic.py script
        """
        self.create_index(index_name="statistics", schema="statistics_schema.json")
        records = self.utils.read_json_from_resources(report_file)
        for record in records:
            ELASTIC.elastic_search.index(index="statistics", body=record)


if __name__ == '__main__':
    ELASTIC = Elastic()
    ELASTIC.create_index()
    ELASTIC.add_user_names()
