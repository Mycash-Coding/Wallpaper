import os
import ctypes
import urllib.request
import json

# Official, stable NASA Astronomy Picture of the Day API (using their public demo key)
url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

try:
    # Fetch data
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())
    
    # Check if the daily asset is actually an image (sometimes it's a video)
    if data.get('media_type') == 'image':
        image_url = data.get('hdurl') or data.get('url')
        
        # Define save path (Your Windows Pictures folder)
        img_dir = os.path.join(os.environ['USERPROFILE'], 'Pictures')
        img_path = os.path.join(img_dir, 'nasa_daily.jpg')
        
        # Download and overwrite the old image
        urllib.request.urlretrieve(image_url, img_path)
        
        # Windows API call to instantly refresh and set the wallpaper
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 3)
        print("Success! Wallpaper updated with today's NASA image.")
    else:
        print("Today's feature is a video. Skipping wallpaper update.")
        
except Exception as e:
    print(f"Error: {e}")
