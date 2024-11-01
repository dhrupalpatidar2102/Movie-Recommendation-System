import pandas as pd
import streamlit as st
import pickle
import numpy
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7d6aa42d58686a4a2787821f069070aa&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    m_List = movie_list.copy()

    recommended_movies = []
    recommended_movies_poster = []
    for i in m_List:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movie_dict = pickle.load(open('Movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
# movie_list = movie_list['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('How would you like to be contacted?',
movies['title'].values)

if st.button('Recommend'):
    name, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])
