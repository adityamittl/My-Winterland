import streamlit as st
import pandas as pd
import pickle

similarity = pickle.load(open('similarity.pkl', 'rb'))

tags_df = pd.read_csv('tags_df.csv')

details_df = pd.read_csv('netflix_titles.csv')

def recommend(title):
    index = tags_df[tags_df['title'] == title].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

    recommendations = []

    for i in distances[1:6]:
        recommendations.append(tags_df.iloc[i[0]].show_id)

    return recommendations

st.image('header.png', use_column_width=True)

option = st.selectbox("Select the movies/shows you've liked", tags_df['title'].values)

if st.button("Recommend"):
    rec = recommend(option)
    
    st.subheader("Recommendations for you:")

    for i in range(5):
        details = details_df[details_df['show_id'] == rec[i]]
        st.header(str(i+1) + '. ' + details['title'].values[0])
        st.write("Description - " + details['description'].values[0])
        st.write("Genre(s) - " + details['listed_in'].values[0])
        st.write("Rating - " + details['rating'].values[0])
        # for handling missing values in dataset
        try:
            star_cast = (details['cast'].values[0]).split(',')[:3]
            st.write("Star Cast - " + star_cast[0] + ", " + star_cast[1] + ", " + star_cast[2])
        except:
            pass
        try:
            st.write("Director - " + details['director'].values[0])
        except:
            pass
        try:
            st.write("Country - " + details['country'].values[0])
        except:
            pass
        
        st.write("")