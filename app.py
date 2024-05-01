import pandas as pd
import streamlit as st
import pickle
import requests
import gzip

def fetch_poster(movie_id):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlNTVlZTlkMTM5NDgwZjlhYjAwMDQwNmE1ZWE5YjdjYyIsInN1YiI6IjY2MTRkOTI3M2Q3NDU0MDE4NTA5MTdjYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.h_STvfivJlKDbL6n-dIUGBrwoy3A35t24-3yD4mYrYk"
    }
    response = requests.get('https://api.themoviedb.org/3/movie/{}?language=en-US'.format(movie_id), headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w780/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load the uncompressed movies_dict.pkl file
with open('movies_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

# Load the compressed similarity.pkl file
with gzip.open('similarity_compressed.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Enter The Movie Name', movies['title'].values,
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
