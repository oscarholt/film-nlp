import requests
from bs4 import BeautifulSoup
import re
import os

URL = 'https://imsdb.com'

genres = ['Action', 'Adventure', 'Animation', 'Comedy',
          'Crime', 'Drama', 'Family', 'Fantasy', 'Film-Noir',
          'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
          'Short', 'Thriller','War', 'Western']

def create_directories(genres):
    for genre in genres:
        dir_path = './categories/' + genre.lower()
        os.makedirs(dir_path, exist_ok = True)
    return True

def get_genre_data(genre):
    genre_data = []
    url = URL + '/genre/' + genre
    
    print(f"Getting genre data for {genre}")
    response = requests.get(url)
    links = BeautifulSoup(response.content, "html.parser").find_all('a', title=True)
    urls = [link for link in links if 'Movie Script' in link['href']]

    for url in urls:
        script = dict()
        script['title'] = generate_script_title(url)
        script['url'] = generate_script_link(script)
        script['filename'] = generate_script_filename(script)
        genre_data.append(script)

    return genre_data

def generate_script_title(url):
    title = re.sub(" Script", "", url['title'])
    if title.endswith(", The"):
        title = "The " + re.sub(", The", "", title)
    return title


def generate_script_link(script):
    link =  re.sub(" ", "-", script['title'])
    return 'https://imsdb.com/scripts/' + link + '.html'

def generate_script_filename(script):
    filename = re.sub(" ", "-", script['title'])
    return filename.lower() + '.txt'

def get_genre_scripts(genre, data):
    for script in data:
        url = script['url']
        path = './categories/' + genre.lower() + '/' + script['filename']

        print(f"Getting script data for {script['title']} from {script['url']}")
        response = requests.get(url)
        
        if response.ok:
            print(f"Response ok for {script['title']}")
            text = BeautifulSoup(response.content, "html.parser").find("pre")
            if text: 
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(text.get_text())
        else:
            print(f"Response not ok for {script['title']}")

def main():
    for genre in genres:
        genre_data = get_genre_data(genre)
        get_genre_scripts(genre, genre_data)

main()
