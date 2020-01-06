"""
This file contains constants used in this module
"""


class Constants:
    """
    This class contains constants used in this module
    """
    name_search_fields = ["name",
                          "name.camel",
                          "name.ngrams",
                          "name.email",
                          "name.porter",
                          "name.word_delimiter",
                          "name.stemmer",
                          "name.stemmed_and_unstemmed",
                          "name.kstem",
                          "name.phonetic",
                          "name.alphanumpermutation",
                          ]

    company_search_fields = ["standard_lucene",
                             "phonetic",
                             "edge_n_gram",
                             # "keyword",
                             "letter",
                             "ngram",
                             "camelcase",
                             # "email",
                             "stemming",
                             "url_email",
                             "text_microsoft"
                             ]
    fields = "fields"
    tp = "tp"
    tn = "tn"
    fp = "fp"
    fn = "fn"
    precision = "precision"
    recall = "recall"
    f1 = "f1"
    retrieved = "retrieved"
    expected = "expected"
    result = "result"
    text = "text"
    flagged_tokens = "flaggedTokens"
    token = "token"
    suggestions = "suggestions"
    score = "score"
    suggestion = "suggestion"
