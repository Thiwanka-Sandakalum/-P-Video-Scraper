# Video Scraper

This Python script allows you to scrape videos from a given profile URL. It utilizes BeautifulSoup for web scraping and requests for making HTTP requests. The script can be run from the command line with options to specify the profile URL and output directory.

## Features

- Download videos from a profile URL.
- Option to specify the output directory.
- Progress bar to show download progress.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your_username/video-scraper.git
```

2. Navigate to the project directory:

```bash
cd video-scraper
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```bash
python scraper.py <profile_url> [--output <output_directory>]
```

Replace `<profile_url>` with the URL of the profile containing videos. Optionally, you can specify the `--output` or `-o` flag followed by the desired output directory.

## Example

```bash
python scraper.py https://www.example.com/profile/videos --output my_downloads
```

This will download videos from the specified profile URL and save them in the `my_downloads` directory.

## Supported Websites

- [TW Pornstars](https://www.twpornstars.com/)

## Dependencies

- BeautifulSoup
- requests
- tqdm

