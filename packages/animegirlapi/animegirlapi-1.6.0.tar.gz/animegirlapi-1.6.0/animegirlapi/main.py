import requests
import random
import os
from typing import Union

def get_info(url):
    """Fetches and returns information for a specific URL from the API."""
    
    with requests.Session() as session:
            response = session.get("https://www.catgirlnexus.xyz/api/references/all_tags.json", timeout=(2, 10)).json()  # Set timeout for the request
    data = response.get(url, {})
    return_value = {
        'tags': {k: v for k, v in data.items() if k != "rating"},
        'rating': data.get("rating")
    }
    return return_value

def get_all_tags():
    """Returns a dictionary of all possible tags and their descriptions."""
    tags = {
        "vampire": "A character with vampiric traits.",
        "gothic": "A character with a dark, gothic style.",
        "demon": "A character with demonic traits.",
        "kawaii": "A character with an extremely cute and endearing appearance.",
        "magical girl": "A character with magical abilities, often with a transformation theme.",
        "romantic": "A character in a romantic or affectionate pose.",
        "bunnygirl": "A character with bunny ears and traits.",
        "catgirl": "A character with cat ears and traits.",
        "foxgirl": "A character with fox ears and traits.",
        "big breast": "A character with a large bust.",
        "heterochromia": "A character with two different-colored eyes, often adding a unique and striking visual trait.",
        "small breast": "A character with a small bust.",
        "yuri": "Content focusing on romantic relationships between women.",
        "multiple girl": "Content involving multiple female characters.",
        "schoolgirl": "A character dressed as a schoolgirl.",
        "elf": "A character with elf-like features.",
        "other animal": "There are other animals in the picture.",
        "feet": "Contains feet images.",
        "puppygirl": "A character with dog ears and traits.",
        "favorites": "Favorites of the owner.",
        "blush": "Contains image of heavy blushing.",
        "maid": "A character dressed in a maid uniform with charming and elegant traits.",
        "loli": "A character depicted as young, petite, and often very cute, embodying a childlike or youthful appearance."
    }
    return tags

def download_image(url, output=None):
    """Downloads an image from the specified URL and saves it to the given path."""
    if output is None:
        output = os.path.basename(url)  # Extracts the filename from the URL
    
    # If output is a file name only, resolve it relative to the current working directory
    if not os.path.isabs(output):
        output = os.path.join(os.getcwd(), output)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output), exist_ok=True)
    
    try:
        # Fetch the image
        with requests.Session() as session:
            response = session.get(url, timeout=(2, 10))  # Set timeout for the request

        # Write the image to the specified path
        with open(output, 'wb') as file:
            file.write(response.content)
        
        print(f"Image successfully downloaded and saved to {output}")
        return {'path': output}  # Return the path for further processing
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
        raise  # Propagate the error

def get_all_images():
    """Fetches and returns all images from the API."""
    with requests.Session() as session:
            response = session.get("https://www.catgirlnexus.xyz/api/references/all_tags.json", timeout=(2, 10))  # Set timeout for the request
    return response.json()

def get_all_ratings():
    """Returns a list of all possible ratings."""
    rating_tags = [
        "suggestive",
        "very suggestive",
        "nsfw",
        "safe"
    ]
    return rating_tags

def get_random_image(number=1, tag: Union[str, tuple, list] = None, rating: Union[str, tuple, list] = None, ignore=False, randomize=False):
    """Gets a random image from the API that matches the specified tag(s) and/or rating(s)."""
    if number > 100:
        raise ValueError("The number of images requested is too high. Please request 100 or fewer images.")
    
    with requests.Session() as session:
        response = session.get("https://www.catgirlnexus.xyz/api/references/all_tags.json", timeout=(2, 10)).json()
    
    filtered_urls = []
    
    # Normalize tag and rating inputs to lists for easier handling
    if isinstance(tag, str):
        tag = [tag]
    if isinstance(rating, str):
        rating = [rating]
    
    # Shuffle the data if randomize is True
    if randomize:
        urls = list(response.keys())
        random.shuffle(urls)
    else:
        urls = response.keys()
    
    # Iterate over the dictionary items
    for url in urls:
        attributes = response[url]
        image_tags = list(attributes.keys())
        image_rating = attributes.get("rating", "")
        
        # Check if the image matches the given tag(s)
        tag_match = True if not tag else any(t in image_tags for t in tag)
        
        # Check if the image matches the given rating(s)
        rating_match = True if not rating else image_rating in rating
        
        # Append URL if both conditions are met
        if tag_match and rating_match:
            filtered_urls.append(url)
        
        # Stop if we've collected enough URLs
        if len(filtered_urls) >= number:
            break
    
    return_value = random.sample(filtered_urls, min(len(filtered_urls), number)) if filtered_urls else []

    if (not return_value or len(return_value) != number) and not ignore:
        print("Warning! The API didn't contain enough images to fit your request. You may contact _.lex0 on Discord to submit if you want more images in the specific tags.\nTo remove this warning insert `ignore=True` in the function")
    
    return return_value