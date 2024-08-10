import streamlit as st
import pickle
import pandas as pd
import requests 

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bbab7e5012ac0c9eb0f64230294088cf&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']




def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

    recommended_movies = []
    recommended_movies_poster = []

    for i in distances[1:6]:
        movie_id_is = movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id_is))
    return recommended_movies , recommended_movies_poster   



st.title('Movie Recommener System')

selected_movie_name = st.selectbox(
    "What would you like to watch today?",
    movies['title'].values,
    index=None,
    placeholder="Please select a movie...",
)

st.button("Reset", type="primary")
if st.button("Recommend"):
    name, poster = recommend(selected_movie_name)


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])    

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])                
else:
    st.write("Goodbye")