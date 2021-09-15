import pandas as pd
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

warnings.filterwarnings('ignore')
df = pd.read_csv('../static/data/movies_meta_summary.csv')
df = df.head(20000)
tvect = TfidfVectorizer(stop_words='english')
tfidf_matrix = tvect.fit_transform(df.overview)
indices = pd.Series(df.index, index=df.title).drop_duplicates()

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df.title.iloc[movie_indices]

s = get_recommendations('The Dark Knight Rises')
print(s)