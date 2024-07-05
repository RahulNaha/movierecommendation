import streamlit as st
import pickle
import pandas as pd
import requests
import os

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4984bbed650a08e16170393abb1d75af&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # assuming your DataFrame has a 'movie_id' column
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Construct paths to the pickle files
movie_dict_path = os.path.join(current_dir, 'movie_dict.pkl')
similarity_path = os.path.join(current_dir, 'similarity.pkl')

# Load the pickle files
movie_dict = pickle.load(open(movie_dict_path, 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open(similarity_path, 'rb'))

st.title('Movie Recommendation System')

option = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(option)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
