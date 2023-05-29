import random
import requests
from PIL import Image
import os
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk

TMDB_API_KEY = "2ab5ae214dc71fefcc2a44cccd9dc190"
OMDB_API_KEY = "e8a55f4d"

def fetch_movie_details(movie_title):
    """Function to fetch movie details, including actor information and streaming service details"""
    try:
        # Search for the movie using TMDb API
        tmdb_url = f"https://api.themoviedb.org/3/search/movie"
        tmdb_params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title
        }
        tmdb_response = requests.get(tmdb_url, params=tmdb_params)
        tmdb_response.raise_for_status()
        tmdb_data = tmdb_response.json()

        # Extract the movie details
        results = tmdb_data.get("results", [])
        if results:
            movie = results[0]
            title = movie.get("title")
            movie_id = movie.get("id")

            # Fetch the actor information using the OMDB API
            omdb_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={movie_id}"
            omdb_response = requests.get(omdb_url)
            omdb_response.raise_for_status()
            omdb_data = omdb_response.json()

            # Extract the actor details
            actors = omdb_data.get("Actors", "Unknown")

            # Fetch the streaming service information
            tmdb_providers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
            tmdb_providers_params = {"api_key": TMDB_API_KEY}
            tmdb_providers_response = requests.get(tmdb_providers_url, params=tmdb_providers_params)
            tmdb_providers_response.raise_for_status()
            tmdb_providers_data = tmdb_providers_response.json()

            # Extract the streaming service information
            streaming_services = []
            results = tmdb_providers_data.get("results", {}).get(str(movie_id), {}).get("flatrate", [])
            for result in results:
                streaming_services.append(result.get("provider_name"))

            # Fetch the poster URL
            poster_url = f"https://image.tmdb.org/t/p/w200{movie.get('poster_path', '')}"

            return {
                "title": title,
                "actors": actors,
                "streaming_services": streaming_services,
                "description": movie.get("overview", "No description available."),
                "poster": poster_url
            }
        else:
            raise ValueError("Movie not found.")
    except requests.exceptions.RequestException as e:
        print("Error occurred during API request:", e)
        return None
    except (KeyError, ValueError) as e:
        print("Error occurred while parsing API response:", e)
        return None
    
# Create a new Tkinter window
window = tk.Tk()
window.title("Movie Details")

# Open the window in full screen
window.attributes('-fullscreen', True)

# Create a label widget for the movie details
details_label = tk.Label(window, text="Movie Details", font=("Helvetica", 16, "bold"))
details_label.pack()

# Create labels for the movie details
title_label = tk.Label(window, text="Title:")
title_label.pack()

actor_label = tk.Label(window, text="Actor:")
actor_label.pack()

description_label = tk.Label(window, text="Description:", wraplength=300)  # Adjust the wrap length as needed
description_label.pack()

# Create an image label for the movie poster
poster_label = tk.Label(window)
poster_label.pack()

def fetch_and_display_movie():
    movie_list = []
    with open("movie_list.txt", "r") as file:
        for line in file:
            movie_list.append(line.strip())

    random_movie = random.choice(movie_list)
    movie_details = fetch_movie_details(random_movie)

    if movie_details:
        title = movie_details["title"]
        actors = movie_details["actors"]
        description = movie_details["description"]
        poster_url = movie_details["poster"]

        # Download the poster image
        response = requests.get(poster_url)
        response.raise_for_status()

        # Save the image to a file
        image_path = os.path.join(os.getcwd(), f"{title}.jpg")
        with open(image_path, "wb") as image_file:
            image_file.write(response.content)

        # Open the image using PIL
        image = Image.open(image_path)
        image.thumbnail((200, 200))  # Resize the image

        # Convert the PIL image to a Tkinter-compatible format
        photo = ImageTk.PhotoImage(image)

                # Delete the image file
        os.remove(image_path)

        # Update the labels and image in the GUI
        title_label.config(text="Title: " + title)
        actor_label.config(text="Actor: " + actors)
        description_label.config(text="Description: " + description)
        poster_label.config(image=photo)
        poster_label.image = photo  # Keep a reference to the image to avoid garbage collection

        # Show a message box with the movie details
        messagebox.showinfo("Movie Details", f"Title: {title}\nActor: {actors}\nDescription: {description}")

    else:
        messagebox.showerror("Error", "Failed to fetch movie details.")

# Create a button to fetch and display movie details
fetch_button = tk.Button(window, text="Fetch Movie", command=fetch_and_display_movie, bg="blue", fg="white")
fetch_button.pack()

# Start the Tkinter event loop
window.mainloop()
