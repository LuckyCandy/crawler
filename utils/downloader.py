import os.path

import requests
from tqdm import tqdm
from common import settings
import os.path
from urllib.parse import urlparse
from utils.logger import get_logger


class Downloader(object):
    def __init__(self, url, store_name):
        self.url = url
        self.store_name = store_name
        self.headers = {}

    def set_request_headers(self, headers: dict):
        self.headers = headers

    def start(self):
        response = requests.get(self.url, stream=True, headers=self.headers)
        # Get the total file size
        file_size = int(response.headers.get("Content-Length", 0))
        # Show the progress bar
        progress = tqdm(total=file_size, unit="iB", unit_scale=True)

        # Write the image to disk
        if not os.path.exists(settings.RESOURCE_PATH):
            os.makedirs(settings.RESOURCE_PATH)

        url_path = urlparse(self.url).path
        _, ext = os.path.splitext(url_path)
        file_name = os.path.join(settings.RESOURCE_PATH, '{0}{1}'.format(self.store_name, ext))
        if os.path.exists(file_name):
            get_logger().warning('要下载的资源【%s】已存在', file_name)
            return
        with open(file_name, 'wb') as f:
            for data in response.iter_content(chunk_size=4096):
                progress.update(len(data))
                f.write(data)

        progress.close()
