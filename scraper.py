import argparse
import logging
import os
from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

def download_video(video_url, dir_, file_name):
    try:
        response = requests.get(video_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        if response.status_code == 200:
            os.makedirs(dir_, exist_ok=True)
            output_path = os.path.join(dir_, f"{file_name}.mp4")

            with open(output_path, 'wb') as file, tqdm(
                desc=f"Downloading {file_name[:10]}.mp4", total=total_size, unit='B', unit_scale=True
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        progress_bar.update(len(chunk))
                        
            logging.info(f"Video '{file_name}' downloaded successfully.\n")
        elif response.status_code == 404:
            logging.warning(f"Video '{file_name}' not found. Skipping...")
        else:
            logging.error(f"Failed to download the video '{file_name}'. Status code: {response.status_code}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def extract_link(url, profile_name, title):
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    video_tag = soup.find(id="video_tag")

    if video_tag and video_tag.find('source'):
        video_source = video_tag.find('source')['src']
        title = ''.join(c for c in title if c.isalnum() or c in [' ', '.'])
        download_video(video_url=video_source, file_name=title, dir_=profile_name)
    else:
        logging.warning("No video source found on the page.")

def get_profile(profile_url, profile_name):
    try:
        res = requests.get(profile_url)
        res.raise_for_status()

        soup = bs(res.text, "html.parser")
        result_set = soup.find_all('a', class_='thumb__link')

        for a_tag in result_set:
            video_page = a_tag.get('href')
            title = a_tag.get('title')[:50]
            extract_link(video_page, profile_name, title)
        logging.info(f"{profile_name} download completed")

    except requests.exceptions.RequestException as req_exc:
        logging.error(f"Request failed: {req_exc}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download videos from a profile URL.")
    parser.add_argument("profile_url", help="URL of the profile containing videos")
    parser.add_argument("--output", "-o", help="Specify the output directory")
    args = parser.parse_args()

    profile_url = args.profile_url
    profile_name = profile_url.split('/')[-2]
    output_dir = args.output or profile_name

    print(f"Downloading videos from {profile_url} to {output_dir} directory...")
    get_profile(profile_url, output_dir)

if __name__ == "__main__":
    main()
