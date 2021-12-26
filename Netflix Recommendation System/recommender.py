import pandas as pd
import numpy as np

df = pd.read_csv('netflix_titles.csv')

df = df.drop(['date_added', 'duration'], axis=1)

def convert_to_list(text):
    try:
        text = text.split(',')
        if(len(text)>5):
            return text[:5]
        else:
            return text
    except:
        return []

df['cast'] = df['cast'].apply(convert_to_list)
df['listed_in'] = df['listed_in'].apply(convert_to_list)
df['director'] = df['director'].apply(convert_to_list)
df['country'] = df['country'].apply(convert_to_list)

df = df.dropna()

def join_names(list_of_names):
    ret = []
    for i in list_of_names:
        ret.append(i.replace(" ",""))
    return ret

df['director'] = df['director'].apply(join_names)
df['cast'] = df['cast'].apply(join_names)
df['country'] = df['country'].apply(join_names)
df['listed_in'] = df['listed_in'].apply(join_names)

# converting remaining columns to a list
df['description'] = df['description'].apply(lambda x: x.split())
df['type'] = df['type'].apply(lambda x: [x])
df['release_year'] = df['release_year'].apply(lambda x: [x])
df['rating'] = df['rating'].apply(lambda x: [x])

# genearting movie/series tags
df['tags'] = df['type'] + df['director'] + df['cast'] + df['country'] + df['release_year'] + df['rating'] + df['listed_in'] + df['description']

# tags_df - a new dataset containing only relevant movie details
tags_df = df[['show_id', 'title', 'tags']]

def truncate(text):
    l = ''
    for i in text:
        l = l + str(i) + ' '
    return l

tags_df['tags'] = tags_df['tags'].apply(truncate)

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=4000,stop_words='english')
vector = cv.fit_transform(tags_df['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)

def recommend(title):
    index = tags_df[tags_df['title'] == title].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(tags_df.iloc[i[0]].title)

recommend('Kota Factory')

import pickle
pickle.dump(similarity,open('similarity.pkl','wb'))

tags_df.to_csv('tags_df.csv', index=False)