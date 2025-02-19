# Flask Movie App README

This README provides an overview of a Flask-based movie application that allows users to search for movies, add them to a personal list, rate them, and write reviews. The application uses The Movie Database (TMDb) API to fetch movie details and stores data in a CSV file.

## Prerequisites

- Python 3.x
- Flask
- Flask-Bootstrap
- Flask-WTF
- Requests
- chardet

## Setup

1. **Clone the repository** (or create a new project and copy the code into it).

2. **Install the required packages**:
    ```sh
    pip install Flask Flask-Bootstrap Flask-WTF requests chardet
    ```

3. **Get an API key** from [The Movie Database (TMDb)](https://www.themoviedb.org/) and replace `"your moviedb api key"` with your actual API key in the script.

4. **Create a CSV file** named `movies.csv` in the project directory with the following headers:
    ```csv
    id,title,year,description,rating,ranking,review,img_url
    ```

## Usage

### Running the Application

1. **Run the Flask application**:
    ```sh
    python your_script_name.py
    ```

2. **Open a web browser** and navigate to `http://127.0.0.1:5000/`.

### Features

#### Home Route (`/`)
- Displays the list of movies sorted by their rating in descending order.
- Movies are ranked based on their rating.

#### Add Movie Route (`/add`)
- A form to search for movies by title.
- Fetches search results from TMDb and displays a list of matching movies.
- Select a movie to add it to the personal list.

#### Find Movie Route (`/find`)
- Fetches detailed information about a selected movie from TMDb.
- Adds the selected movie to the CSV file and redirects to the rate movie page.

#### Rate Movie Route (`/edit`)
- A form to rate the movie and write a review.
- Updates the CSV file with the rating and review.

#### Delete Movie Route (`/delete`)
- Removes the selected movie from the CSV file.

### Forms

#### FindMovieForm
- **title**: Input field for the movie title.
- **submit**: Submit button to add the movie.

#### RateMovieForm
- **rating**: Input field for the movie rating out of 10.
- **review**: Input field for the movie review.
- **submit**: Submit button to save the rating and review.

## File Descriptions

### Main Script
- **Imports necessary libraries**: Flask, Bootstrap, WTForms, Requests, chardet, CSV.
- **Defines Flask application**.
- **Sets up forms** using WTForms.
- **Defines helper functions**: `read_movies_from_csv` and `write_movies_to_csv`.
- **Defines routes**: `/`, `/add`, `/find`, `/edit`, `/delete`.

### Helper Functions

#### `read_movies_from_csv()`
- Reads the movies from the CSV file.
- Detects the file encoding using chardet.
- Cleans up the movie data by removing problematic characters.

#### `write_movies_to_csv(movies)`
- Writes the list of movies to the CSV file with UTF-8 encoding.

### Templates
- **index.html**: Displays the list of movies with their details.
- **add.html**: Form to search and add movies.
- **select.html**: Displays the search results to select a movie.
- **edit.html**: Form to rate and review the selected movie.

## Conclusion

This Flask application provides a simple and interactive way to manage a personal list of movies, including searching for movies, adding them, rating, and reviewing them. By integrating with TMDb API, it offers detailed movie information and enhances the user experience. Customize the templates and styles as needed to fit your requirements.
