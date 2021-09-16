import numpy as np
import pandas as pd
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

warnings.filterwarnings('ignore')
cosine_sim_loaded = False
cosine_sim = np.array([])
df = pd.DataFrame()

def get_cosine_sim():
    global cosine_sim, cosine_sim_loaded, df
    if cosine_sim_loaded:
        return
    df = pd.read_csv('static/data/movies_meta_summary.csv')

    tvect = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tvect.fit_transform(df.overview)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim_loaded = True

def get_recommendations(index):
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_list = [df.title.iloc[i[0]] for i in sim_scores]
    title = df.title[index]
    return movie_list, title

def get_movie_index(title):
    indices = pd.Series(df.index, index=df.title)
    try:
        index = indices[title]
    except:
        index = -1
    return index