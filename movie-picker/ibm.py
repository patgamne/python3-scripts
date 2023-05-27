import random
import requests
from PIL import Image
import os

API_KEY = "e8a55f4d"

def fetch_movie_details(movie_title):
    """Function to fetch movie details using the OMDB API"""
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_title}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        if data.get("Response") == "False":
            raise ValueError(data.get("Error", "Unknown error occurred."))

        title = data.get("Title", "Unknown")
        actor = data.get("Actors", "Unknown")
        description = data.get("Plot", "No description available.")
        poster_url = data.get("Poster", "")
        movie_details = {
            "title": title,
            "actor": actor,
            "description": description,
            "poster": poster_url
        }
        return movie_details
    except requests.exceptions.RequestException as e:
        print("Error occurred during API request:", e)
        return None
    except (KeyError, ValueError) as e:
        print("Error occurred while parsing API response:", e)
        return None

# Example usage
movie_list = []
with open("movie_list.txt", "r") as file:
    for line in file:
        movie_list.append(line.strip())

random_movie = random.choice(movie_list)
movie_details = fetch_movie_details(random_movie)

if movie_details:
    title = movie_details["title"]
    actor = movie_details["actor"]
    description = movie_details["description"]
    poster_url = movie_details["poster"]

    # Download the poster image
    response = requests.get(poster_url)
    response.raise_for_status()

    # Save the image to a file on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    image_path = os.path.join(desktop_path, f"{title}.jpg")
    with open(image_path, "wb") as image_file:
        image_file.write(response.content)

    # Open the image using the default image viewer
    Image.open(image_path).show()

    # Print the movie details
    print(f"Title: {title}")
    print(f"Actor: {actor}")
    print(f"Description: {description}")
else:
    print("Failed to fetch movie details.")
