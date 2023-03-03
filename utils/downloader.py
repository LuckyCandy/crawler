import requests
from tqdm import tqdm


class Downloader(object):
    def __new__(cls, url):
        cls.url = url

    def start(self):
        response = requests.get(self.url, stream=True)
        # Get the total file size
        file_size = int(response.headers.get("Content-Length", 0))
        # Show the progress bar
        progress = tqdm(total=file_size, unit="iB", unit_scale=True)

        # Write the image to disk
        with open('image.jpg', 'wb') as f:
            for data in response.iter_content(chunk_size=4096):
                progress.update(len(data))
                f.write(data)

        progress.close()
