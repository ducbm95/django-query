from request_gg import RequestGG
from pyvi.pyvi import ViTokenizer
import pickle

# optional
import psycopg2

from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV

import numpy as np


class QueryClassification:

  def __init__(self):
    self.requestGG = RequestGG()
    self.tfidf_vectorizer = pickle.load(open("backend/tfidf_vectorizer.pickle", "rb"))
    self.clf = pickle.load(open("backend/classifier.pickle", "rb"))
    self.classes = self.clf.classes_

    # connect Postgres
    self.conn = None
    try:
      self.conn = psycopg2.connect("dbname='postgres' user='postgres' password='12345678'")
    except:
      print "Error when connect to DB"
    self.cur = self.conn.cursor()

    # self.queries_dict_tokenized = pickle.load(open("queries_dict_tokenized_minimized_2.pickle", "rb"))

  def cal_tfidf(self, query):
    query = unicode(query).lower()

    self.cur.execute(
      unicode("""
        SELECT query_data FROM query
        WHERE query = %(query)s"""),
      {"query": query})
    tokenized_text = self.cur.fetchone()
    # tokenized_text = self.queries_dict_tokenized[query]

    if tokenized_text != None:
      tokenized_text = tokenized_text[0]
    else:
      enriched_text = self.requestGG.getStandardName(unicode(query))
      tokenized_text = ViTokenizer.tokenize(enriched_text)

    tfidf = self.tfidf_vectorizer.transform([tokenized_text])
    return tfidf

  def predict(self, query):
    tfidf = self.cal_tfidf(query)
    predicted_category = self.clf.predict(tfidf) # for LinearSVC
    # predicted_category = self.clf.predict(tfidf.toarray())
    return predicted_category[0]

  # predict "n" best category for "query"
  def predict_best_classes(self, query, n = 3):
    tfidf = self.cal_tfidf(query)
    arr_proba = self.clf.predict_proba(tfidf) # for LinearSVC
    # arr_proba = self.clf.predict_proba(tfidf.toarray())
    np_arr_proba = np.array(arr_proba[0])

    # tra ve top n index cua cac class co score lon nhat, mac dinh n = 3
    top_label_index = np_arr_proba.argsort()[-n:][::-1]

    list_predicted_category = []
    for idx in top_label_index:
      list_predicted_category.append(self.classes[idx])
    return list_predicted_category

  def predict_best_classes_with_score(self, query, n = 3):
    tfidf = self.cal_tfidf(query)
    arr_proba = self.clf.predict_proba(tfidf) # for LinearSVC
    # arr_proba = self.clf.predict_proba(tfidf.toarray())
    np_arr_proba = np.array(arr_proba[0])

    # tra ve top n index cua cac class co score lon nhat, mac dinh n = 3
    top_label_index = np_arr_proba.argsort()[-n:][::-1]

    list_predicted_category = []
    for idx in top_label_index:
      list_predicted_category.append({ 'class' : self.classes[idx], 'score' : np_arr_proba[idx]})
    return list_predicted_category
