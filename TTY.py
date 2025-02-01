import os
import time
import logging
from dotenv import load_dotenv
from youtubesearchpython import VideosSearch
from pytube import Search
from ytmusicapi import YTMusic
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    filename="tty.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to read the input text file
def read_input_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tracks = file.read().splitlines()
    return tracks

# Function to search YouTube Music using ytmusicapi
def search_ytmusicapi(query):
    try:
        ytmusic = YTMusic()
        results = ytmusic.search(query, filter="songs", limit=1)
        if results:
            return f"https://music.youtube.com/watch?v={results[0]['videoId']}"
    except Exception as e:
        logging.error(f"Error with ytmusicapi: {e}")
    return None

# Function to search YouTube using youtubesearchpython
def search_youtube_search_python(query):
    try:
        videos_search = VideosSearch(query, limit=1)
        results = videos_search.result()
        if results and "result" in results and results["result"]:
            return results["result"][0]["link"]
    except Exception as e:
        logging.error(f"Error with youtubesearchpython: {e}")
    return None

# Function to search YouTube using pytube
def search_pytube(query):
    try:
        search = Search(query)
        if search.results:
            return search.results[0].watch_url
    except Exception as e:
        logging.error(f"Error with pytube: {e}")
    return None

# Function to search YouTube Music using multiple libraries
def search_youtube_music(track):
    # Try ytmusicapi first
    url = search_ytmusicapi(track)
    if url:
        return url

    # If ytmusicapi fails, try youtubesearchpython
    url = search_youtube_search_python(track)
    if url:
        return url

    # If youtubesearchpython fails, try pytube
    url = search_pytube(track)
    if url:
        return url

    # If all libraries fail, return "No result"
    return "No result"

# Function to save the results to a text file
def save_results(results, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for result in results:
            file.write(f"{result}\n")

# Main script
if __name__ == "__main__":
    # Input and output file paths
    input_file = "STT_playlist.txt"
    output_file = "YTMusic_playlist.txt"

    # Read the input file
    tracks = read_input_file(input_file)
    print(f"Found {len(tracks)} tracks in the input file.")

    # Search for each track
    results = []
    save_interval = 10
    for i, track in enumerate(tqdm(tracks, desc="Processing tracks")):
        print(f"\nProcessing track {i+1}/{len(tracks)}: {track}")
        result = search_youtube_music(track)
        results.append(f"{track}: {result}")
        time.sleep(1)  # Add a delay to avoid rate limits

        # Save results periodically
        if (i + 1) % save_interval == 0:
            save_results(results, output_file)
            print(f"Progress saved: {i+1}/{len(tracks)} tracks processed.")

    # Save final results
    save_results(results, output_file)
    print(f"Results saved to {output_file}.")