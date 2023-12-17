import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
indc = pickle.load(open('indices.pkl', 'rb'))
movies_list = movies['original_title'].values

# Function to fetch movie poster from The Movie Database (TMDb) API
def fetch_poster(movie_id):
    # API request to retrieve movie information
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a3cdfdc415ae12dc0ce1e65d46678daf&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    
    # Extracting poster path from API response
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# App header
st.header('Movie Recommender System')

# Predefined image URLs for the Image Carousel Component
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]
# Rendering the Image Carousel Component
imageCarouselComponent(imageUrls=imageUrls, height=200)

# Dropdown for selecting a movie
selectvalue = st.selectbox('Select movie from dropdown or type it', movies_list)

# Function to provide movie recommendations based on similarity scores
def recs(title, cosine_sim=similarity):
    # Find the index of the movie matching the provided title
    idx = indc[title]

    # Gather the similarity scores for all movies with respect to the given movie
    similarity_scores = list(enumerate(similarity[idx]))

    # Arrange the movies in descending order based on their similarity scores
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Retrieve the scores of the 5 most similar movies (excluding the movie itself)
    similarity_scores = similarity_scores[1:11]

    movie_indices = []
    movie_poster = []

    # Extract the indices and poster of the top 5 most similar movies
    for i in similarity_scores:
        movies_id = movies.iloc[i[0]].id
        movie_indices.append(i[0])
        movie_poster.append(fetch_poster(movies_id))

    # Provide the titles and poster of the top 5 most similar movies
    top_movies = movies['title'].iloc[movie_indices]
    poster = movie_poster

    return top_movies.tolist(), poster

# Button to trigger the display of movie recommendations
if st.button('Show Recommendations'):
    movie_name, movie_poster = recs(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])