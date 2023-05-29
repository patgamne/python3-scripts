import requests
from bs4 import BeautifulSoup

# Function to scrape movie titles from IMDb
def scrape_movie_titles():
    url = "https://www.imdb.com/search/title/?release_date=2000-01-01,2023-12-31&start={}&ref_=adv_nxt"
    titles = []

    for start in range(1, 1000, 50):  # Assuming a maximum of 5000 movies
        response = requests.get(url.format(start))
        soup = BeautifulSoup(response.text, "html.parser")
        movie_tags = soup.find_all("h3", class_="lister-item-header")

        for tag in movie_tags:
            title = tag.a.text
            titles.append(title)

    return titles

# Scrape movie titles
titles = scrape_movie_titles()

# Save titles to a .txt file
with open("movie_list.txt", "w") as file:
    for title in titles:
        file.write(title + "\n")

print("Movie titles saved to movie_titles.txt")
