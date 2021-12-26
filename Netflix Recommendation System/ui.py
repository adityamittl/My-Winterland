import streamlit as st
import pandas as pd
import pickle
import bs4 as BeautifulSoup
import requests

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

def get_poster(name):
    name = name.replace(" ","+")
    base_url = "https://www.imdb.com"
    url = "https://www.imdb.com/find?q="+name
    page = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(page.content, "html.parser")
    res = soup.find_all("table",class_ = 'findList')[0]
    s_url = res.find(class_ = "result_text").find('a')['href']
    page2 = requests.get(base_url+s_url)
    soup2 = BeautifulSoup.BeautifulSoup(page2.content,"html.parser")
    poster_url = BeautifulSoup.BeautifulSoup(requests.get(base_url+soup2.find_all("a",class_="ipc-lockup-overlay ipc-focusable")[0]['href']).content,"html.parser").find_all(class_="MediaViewerImagestyles__PortraitContainer-sc-1qk433p-2 iUyzNI")[0].find("img").attrs["src"]
    return poster_url

st.image('header.png', use_column_width=True)

option = st.selectbox("Select the movies/shows you've liked", tags_df['title'].values)

if st.button("Recommend"):
    recomendations = recommend(option)
    st.subheader("Recommendations for you:")

    for i in range(5):
        col = st.columns([1.15, 2])
        details = details_df[details_df['show_id'] == recomendations[i]]
        col[0].image(get_poster(details['title'].values[0]),use_column_width=True, caption=details['title'].values[0])
        col[1].subheader(str(i+1) + '. ' + details['title'].values[0])
        col[1].write("Description - " + details['description'].values[0])
        col[1].write("Genre(s) - " + details['listed_in'].values[0])
        col[1].write("Rating - " + details['rating'].values[0])
        # for handling missing values in dataset
        try:
            star_cast = (details['cast'].values[0]).split(',')[:3]
            col[1].write("Star Cast - " + star_cast[0] + ", " + star_cast[1] + ", " + star_cast[2])
        except:
            pass
        try:
            col[1].write("Director - " + details['director'].values[0])
        except:
            pass
        try:
            col[1].write("Country - " + details['country'].values[0])
        except:
            pass
        
