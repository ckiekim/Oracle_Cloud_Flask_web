import pandas as pd
import warnings, joblib

warnings.filterwarnings('ignore')
df = pd.read_csv('../static/data/movies_meta_summary.csv')
df = df.head(20000)
indices = pd.Series(df.index, index=df.title).drop_duplicates()
print('start loading')
cos_sim = joblib.load('../static/data/movie_cos_sim.pkl')
print('loaded')

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df.title.iloc[movie_indices]

s = get_recommendations('The Dark Knight Rises')
print(s)