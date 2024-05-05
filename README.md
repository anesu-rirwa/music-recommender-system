# Assignment 2

## Group Members

- Victor Marisa R207764L HAI
- Anesu Rirwa R204432D HAI
- Tariro Gwandiwa R206546B HAI
- Perfect-Princess Makuwerere R204448U HAI

## Content Based Music Recommender App

This Streamlit app recommends songs based on their characteristics such as valence, year, acousticness, etc. This music recommender system is **Content-Based**. You can provide a song, and the app will recommend similar songs based on the features of the provided song.

## How to Use

1. **Enter a Song Name**: Enter the name of a song you like in the text box below.
2. **Select Number of Recommendations**: Use the slider to select the number of songs you want to be recommended.
3. **Click Recommend**: Click the "Recommend" button to get your recommendations.

## Music Recommender Prompt

- Input for song name: Enter a song name in the provided text box.
- Slider to select the number of recommendations: Adjust the slider to choose the number of songs you want to be recommended.
- Button to recommend songs: Click the "Recommend" button to get your recommendations.

## About the Dataset

This dataset covers songs from [start year] to [end year]. The dataset used for this recommender system contains information about various songs including their audio features, such as valence, acousticness, energy, etc., as well as other metadata like artist name, release year, and popularity.

## How to Run Locally

To run this app locally, follow these steps:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/repository-name.git
   ```

2. Navigate to the project directory:
    ```bash
   cd music-recommender
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

The app should open in your default web browser. You can now use the music recommender app locally on your machine.

## Conclusion

The Music Recommender App leverages content-based filtering to recommend songs based on their characteristics such as valence, year, acousticness, etc. By analyzing the features of a provided song, the app identifies similar songs from the dataset and presents them to the user.

With an intuitive user interface, users can easily input their favorite song, select the number of recommendations they desire, and receive a list of suggested songs that share similar attributes.
