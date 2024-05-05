import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from scipy.spatial.distance import cdist
import plotly.express as px

# Load your data
data = pd.read_csv("data.csv")

# List of numerical columns to consider for similarity calculations
number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
               'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

# Function to retrieve song data for a given song name
def get_song_data(name, data):
    try:
        return data[data['name'].str.lower() == name.lower()].iloc[0]
    except IndexError:
        return None

# Function to calculate the mean vector of a list of songs
def get_mean_vector(song_list, data):
    song_vectors = []
    for song in song_list:
        song_data = get_song_data(song['name'], data)
        if song_data is None:
            print(f"Warning: {song['name']} does not exist in the dataset")
            return None
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)
    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)

# Function to recommend songs based on a list of seed songs
def recommend_songs(seed_song, data, n_recommendations=10):
    metadata_cols = ['name', 'artists', 'year']
    song_center = get_mean_vector([seed_song], data)
    
    # Return an empty list if song_center is missing
    if song_center is None:
        return []
    
    # Normalize the song center
    normalized_song_center = min_max_scaler.transform([song_center])
    
    # Standardize the normalized song center
    scaled_normalized_song_center = standard_scaler.transform(normalized_song_center)
    
    # Calculate Euclidean distances and get recommendations
    distances = cdist(scaled_normalized_song_center, scaled_normalized_data, 'euclidean')
    index = np.argsort(distances)[0]
    
    # Filter out seed song and duplicates, then get the top n_recommendations
    rec_songs = []
    for i in index:
        song_name = data.iloc[i]['name']
        if song_name != seed_song['name'] and song_name not in [song['name'] for song in rec_songs]:
            rec_songs.append(data.iloc[i])
            if len(rec_songs) == n_recommendations:
                break
    
    return pd.DataFrame(rec_songs)[metadata_cols].to_dict(orient='records')

# Normalize the song data using Min-Max Scaler
min_max_scaler = MinMaxScaler()
normalized_data = min_max_scaler.fit_transform(data[number_cols])

# Standardize the normalized data using Standard Scaler
standard_scaler = StandardScaler()
scaled_normalized_data = standard_scaler.fit_transform(normalized_data)

# Streamlit app
st.title('Music Recommender')

st.write("""
This app recommends songs based on their characteristics such as valence, year, acousticness, etc. This music recommender system is **Content-Based**. You can provide a song, and the app will recommend similar songs based on the features of the provided song.
""")

st.header('How to Use')

st.write("""
1. **Enter a Song Name**: Enter the name of a song you like in the text box below.
2. **Select Number of Recommendations**: Use the slider to select the number of songs you want to be recommended.
3. **Click Recommend**: Click the "Recommend" button to get your recommendations.
""")

st.header('Music Recommender Prompt')

# Input for song name (use st.text_input)
song_name = st.text_input("Enter a song name:")

# Slider to select the number of recommendations
n_recommendations = st.slider("Select the number of recommendations:", 1, 30, 10)

# Convert input to lowercase
song_name = song_name.lower().strip()

# Button to recommend songs
if st.button('Recommend'):
    if not song_name:
        st.warning("Please enter a song name.")
    else:
        # Get song data
        seed_song = {'name': song_name}
        
        # Call the recommend_songs function
        recommended_songs = recommend_songs(seed_song, data, n_recommendations)
        
        if not recommended_songs:
            st.warning("No recommendations available based on the provided song.")
        else:
            # Convert the recommended songs to a DataFrame
            recommended_df = pd.DataFrame(recommended_songs)
            
            # Display the recommended songs as a table
            st.subheader('Recommended Songs')
            st.table(recommended_df[['name', 'artists', 'year']])

            # Convert the recommended songs to a DataFrame
            recommended_df = pd.DataFrame(recommended_songs)
            
            # Create a bar plot of recommended songs by name
            recommended_df['text'] = recommended_df.apply(lambda row: f"{row.name + 1}. {row['name']} by {row['artists']} ({row['year']})", axis=1)
            fig = px.bar(recommended_df, y='name', x=range(len(recommended_df), 0, -1), title='Recommended Songs', orientation='h', color='name', text='text')
            fig.update_layout(xaxis_title='Recommendation Rank', yaxis_title='Songs', showlegend=False, uniformtext_minsize=20, uniformtext_mode='show', yaxis_showticklabels=False, height=500, width=800)
            fig.update_traces(width=1)
            st.plotly_chart(fig)

st.header('About the Dataset')

st.write("""
This dataset covers songs from {} to {}. The dataset used for this recommender system contains information about various songs including their audio features, such as valence, acousticness, energy, etc., as well as other metadata like artist name, release year, and popularity.

""".format(data['year'].min(), data['year'].max()))

st.write("Let's explore some insights from the dataset:")

# Display the top songs as a table
st.subheader('Top Songs by Popularity')
top_songs_table = data.nlargest(20, 'popularity')[['name', 'artists', 'year', 'popularity']]
st.table(top_songs_table)

# Convert release_date to datetime and extract decade
data['release_date'] = pd.to_datetime(data['release_date'])
data['release_decade'] = (data['release_date'].dt.year // 10) * 10

# Count the number of songs per decade
decade_counts = data['release_decade'].value_counts().sort_index()

# Display the number of songs per decade as a table
st.subheader('Number of Songs per Decade')
decade_table = pd.DataFrame({'Decade': decade_counts.index, 'Number of Songs': decade_counts.values})
st.table(decade_table)
