import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


def softmax(x):
    """Функция для создания вероятностного распределения"""
    proba = np.exp(-x)
    return proba / sum(proba)


class NeighborSampler(BaseEstimator):
    """Класс для случайного выбора одного из ближайших соседей"""

    def __init__(self, k=5, temperature=1.0):
        self.k = k
        self.temperature = temperature

    def fit(self, X, y):
        self.tree_ = BallTree(X)
        self.y_ = np.array(y)

    def predict(self, X, random_state=None):
        distance, indices = self.tree_.query(X, return_distance=True, k=self.k)
        result = []
        for distance, index in zip(distance, indices):
            result.append(np.random.choice(index, p=softmax(distance * self.temperature)))
        return self.y_[result]


good = pd.read_csv('./files/good.tsv', encoding='windows-1251', sep='\t')
svd = TruncatedSVD(n_components=150)
ns = NeighborSampler()

vectorizer = TfidfVectorizer()
vectorizer.fit(good.context_0.values.astype('U'))
matrix_big = vectorizer.transform(good.context_0.values.astype('U'))
svd.fit(matrix_big)
matrix_small = svd.transform(matrix_big)
ns.fit(matrix_small, good.reply)
pipe = make_pipeline(vectorizer, svd, ns)


def search_reply(msg):
    return (pipe.predict([msg]))[0]
